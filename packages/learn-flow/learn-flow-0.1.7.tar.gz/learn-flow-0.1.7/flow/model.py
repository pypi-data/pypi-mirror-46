# -*- coding: utf-8 -*-
"""
module model.py
--------------------
Definition of the machine learning model for the task.
"""
import tensorflow as tf
import numpy as np
from blinker import signal
from .config.config import Config
from .learner import DefaultLearner
from .dataset import Dataset
import time


class Inputs(object):
    def __init__(self):
        pass


class Outputs(object):
    def __init__(self):
        pass


class Model(object):
    """ Project main class.
    """
    # def __init__(self, inputs_config, train_dataset: Dataset=None, valid_dataset: Dataset=None, test_dataset: Dataset=None, config: Config=None):

    def __init__(self, inputs_config, config: Config=None):
        """
        Main module initialization.
        :param inputs_config: inputs shapes, types and names definitions. **keys**: name, output_types, output_shapes
                              **format**:
                              {
                                names: (tuple of strings. variable names),
                                output_types: (tuple of tf.Dtype. foreach variable),
                                output_shapes= (tuple of tf.TensorShape. foreach variable)
                              }
        :type inputs_config: dict
        :param config: a configuration object.
        :type config: Config
        """
        self.config = config
        self._inputs_config = inputs_config
        # datasets
        self._train_dataset = None
        self._valid_dataset = None
        self._test_dataset = None

        self.inputs = Inputs()
        # set in _ get_model
        self.outputs = Outputs()
        self._losses = list()
        self._metrics = list()

        with tf.variable_scope("learning_phase", reuse=tf.AUTO_REUSE):
            self._is_training_phase = tf.get_variable(
                name="is_training_phase",
                dtype=tf.bool,
                initializer=False,
                trainable=False,

            )

        self._handle = tf.placeholder(tf.string, shape=[])
        self._iter = None

        self._is_session_initialized = False
        self._get_inputs()
        # outputs and model initialization
        self.get_model_spec()
        self._initialize_train_callbacks()

    def _initialize_train_callbacks(self):
        """self training callbacks initialization."""
        self.before_session_initialization = signal("before_session_initialization")

    def _get_inputs(self):
        """
        Initializes the input within the inputs_config and dataset definitions.
        """
        # if any dataset was provided
        # if ds is not None:
        out_types = list()
        out_shapes = list()
        batch_size = int(self.config.get("flow.batch_size", 1))
        for tensor_type, tensor_shape in zip(
                self._inputs_config["output_types"],
                self._inputs_config["output_shapes"]
        ):
            tensor_shape = tensor_shape.as_list()
            # adds the batch_size to the tensor shape definition
            tensor_shape = tf.TensorShape([batch_size] + tensor_shape)
            out_types.append(tensor_type)
            out_shapes.append(tensor_shape)

        # then it initializes the ds_iterator
        self._iter = tf.data.Iterator.from_structure(
            output_types=tuple(out_types),
            output_shapes=tuple(out_shapes)
        )
        # and then set it to the models inputs attribute
        inputs = self._iter.get_next()
        # for each variable name and tensor
        for tensor_name, tensor in zip(self._inputs_config["names"], inputs):
            setattr(self.inputs, tensor_name, tensor)

    def get_model_spec(self, *args, **kwargs):
        """
        Layers and model definition
        :return: a compiled model
        """
        pass

    def fit(self, train_dataset: Dataset, valid_dataset: Dataset=None, optimizer=None, learner=DefaultLearner):
        tf.keras.backend.set_learning_phase(1)

        # setting model iterator into dataset
        self._train_dataset = train_dataset
        self._valid_dataset = valid_dataset
        if self._train_dataset is not None:
            self._train_dataset.set_iterator(self._iter)
        if self._valid_dataset is not None:
            self._valid_dataset.set_iterator(self._iter)

        outs = self._prepare_outputs(step="train")
        if optimizer is None:
            optimizer = tf.train.GradientDescentOptimizer(tf.Variable(0.001))
        learner = learner(self, outs, optimizer)
        # TODO prepare inputs: it could be possible to pass the inputs as parameters.
        learner.fit()

    def _initialize_session(self):
        """Default session initialization function."""
        if not self._is_session_initialized:
            # tf global variables initialization (session variables initialization)
            sess = tf.get_default_session()
            sess.run(tf.global_variables_initializer())
            self._is_session_initialized = True

    def _prepare_outputs(self, step="train"):
        """Builds the outputs dictionary that is used during the model fitting."""
        outputs = dict()
        outputs["loss"] = tf.add_n(self._losses, name="loss")

        for m in self._losses:
            name = m.name.split(":")[0]
            if name not in outputs:
                if step == "train" and not name.startswith("valid_"):
                    outputs[name] = m
                elif step is not "train":
                    outputs[name] = m

        for m in self._metrics:
            name = m.name.split(":")[0]
            if name not in outputs:
                if step == "train" and not name.startswith("valid_"):
                    outputs[name] = m
                elif step is not "train":
                    outputs[name] = m

        return outputs

    def evaluate(self, dataset: Dataset):
        """
        Returns the loss value & metrics values for the model in test mode.
        Computation is done in batches.
        """
        self._valid_dataset = dataset
        if self._valid_dataset is not None:
            self._valid_dataset.set_iterator(self._iter)

        # loads model if it is not initialized.
        model_path = self.config.get("flow.PREMODEL", None)
        if not self._is_session_initialized:
            self.load(model_path)
            self._is_session_initialized = True

        # old_learning_phase = tf.keras.backend.learning_phase()
        # tf.keras.backend.set_learning_phase(0)
        # TODO: deal with inputs and/or dataset as input.
        self._valid_dataset.get_iterator_initializer(None)
        self._valid_dataset.initialize_iterator(None)

        # ensures that learning_pahse is False
        self.is_training_phase = False

        sess = tf.get_default_session()
        outs = self._prepare_outputs(step="validation")

        # builds a dictionary containing a key for each step output.
        # The outputs of each learning step is stored on this dictionary.
        accumulators = dict()
        for output_name in outs.keys():
            accumulators[output_name] = list()

        try:
            while True:
                ret = sess.run(
                    fetches=outs
                )
                # accumulate outputs
                for key, val in ret.items():
                    accumulators[key].append(val)

        except tf.errors.OutOfRangeError:
            pass

        results = dict()
        for output_name, output_vals in accumulators.items():
            results[output_name] = np.mean(output_vals)

        # reseting learning phase
        # tf.keras.backend.set_learning_phase(old_learning_phase)
        return results

    def load(self, path):
        """
        Loads a saved model.
        :param path: the saved model path.
        """

        sess = tf.get_default_session()
        saver = tf.train.Saver()
        print("restoring model....")
        saver.restore(
            sess,
            path
        )

    def predict(self, dataset: Dataset, outputs):

        self._valid_dataset = dataset
        if self._valid_dataset is not None:
            self._valid_dataset.set_iterator(self._iter)

        model_path = self.config.get("flow.PREMODEL", None)
        if not self._is_session_initialized:
            self.load(model_path)
            self._is_session_initialized = True

        # todo deal with inputs
        self._valid_dataset.get_iterator_initializer(None)
        self._valid_dataset.initialize_iterator(None)

        self.is_training_phase = False
        # old_learning_phase = tf.keras.backend.learning_phase()
        # tf.keras.backend.set_learning_phase(0)
        # predict
        sess = tf.get_default_session()
        # backward pass
        results = sess.run(
            fetches=outputs,
        )
        # reseting learning phase
        # tf.keras.backend.set_learning_phase(old_learning_phase)
        return results

    @property
    def is_training_phase(self):
        if self._is_session_initialized:
            sess = tf.get_default_session()
            is_training = sess.run(self._is_training_phase)
            return is_training
        else:
            return False

    @is_training_phase.setter
    def is_training_phase(self, value):
        sess = tf.get_default_session()
        # if session was not initialized yet
        # then initialize the is_learning_phase variable
        if not self._is_session_initialized:
            init_phase_op = tf.variables_initializer([self._is_training_phase])
            sess.run(init_phase_op)
        # assing the new phase value to the variable
        sess.run(tf.assign(self._is_training_phase, value))
