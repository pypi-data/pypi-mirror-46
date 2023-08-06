# -*- coding: utf-8 -*-
"""
module learner.py
--------------------
A base class definition for the learner class.
The default learner defines steps for the learning procedure.
"""
import tensorflow as tf
import numpy as np
from blinker import signal
import time


class ModelValidator(object):
    """
    Default Model Validation runner.
    """
    def __init__(self, model):
        self.model = model
        self._init_callbacks()
        # connect to the on_epoch_end callback
        self.validate_sig.connect(self.validate_model, weak=False)

    def _init_callbacks(self):
        self.validate_sig = signal("validate_sig")
        self._on_validate_begin = signal("on_validate_begin")
        self._on_validate_end = signal("on_validate_end")

    def validate_model(self, sender):
        # re-triggers the on_validate_begin event
        self._on_validate_begin.send(sender)
        # ensures that learning_pahse is False
        self.model.is_training_phase = False
        results = self.evaluate()
        for key, value in results.items():
            if key.startswith("valid_"):
                sender.current_state[key] = value
            else:
                sender.current_state["valid_" + key] = value
        # re-trigger the on_validate_end event
        self._on_validate_end.send(sender)

    def evaluate(self):
        results = self.model.evaluate(self.model._valid_dataset)
        return results


class DefaultLearner(object):
    """
    Defines the default learning steps and procedures for fitting models.
    """
    def __init__(self, model, outputs, optimizer, loss_name="loss"):
        """
        Default learner initializer.
        :param model: reference to the model object
        :param outputs: a dictionary of outputs.
        :param optimizer: the optimizer to be used.
        :param loss_name: loss tensor name.
        """
        self.model = model
        self.outputs = outputs
        self.optimizer = optimizer
        # self._update_opt = update_opt
        self._update_opt = optimizer.minimize(outputs[loss_name])

        self.validator = ModelValidator(self.model)

        self.current_state = dict()
        # flag used to signaling when it should stop learning loop.
        self._stop_flag = False
        self._initialize_train_callbacks()
        self.before_session_initialization.send(self.model)
        self._initialize_session()

    def _initialize_train_callbacks(self):
        """self training callbacks initialization."""
        self.validate_sig = signal("validate_sig")
        self.on_epoch_begin = signal("on_epoch_begin")
        self.on_epoch_end = signal("on_epoch_end")
        self.on_batch_begin = signal("on_batch_begin")
        self.on_batch_end = signal("on_batch_end")
        self.on_train_begin = signal("on_train_begin")
        self.on_train_end = signal("on_train_end")
        self.before_session_initialization = signal("before_session_initialization")

    def _get_accumulators(self, outputs:dict):
        """
        builds and returns a dictionary containing a key for each step output.
        The outputs of each learning step is stored on this dictionary.
        :param outputs: A dictionary containing the learning step outputs.
        """
        accumulators = dict()
        for output_name in outputs.keys():
            accumulators[output_name] = list()
        return accumulators

    def _aggregate_accumulators(self, accumulators:dict):
        """
        Averages all learning step outputs for one epoch.
        :param accumulators: epoch outputs values.
        """
        # on epoch end triggers
        for output_name, output_vals in accumulators.items():
            self.current_state[output_name] = np.mean(output_vals)

    def epoch_fit_loop(self, outputs):
        """
        Fit inner loop for one learning epoch.
        :param inputs: a dictionary of inputs.
        :param outputs: a dictionary of outputs.
        """
        accumulators = self._get_accumulators(outputs)
        try:
            # ensures training phase is True
            self.model.is_training_phase = True
            while True:
                # on batch begin triggers
                self.on_batch_begin.send(self)
                # run session and and perform learning step.
                batch_outs = self.learn_step(outputs)
                # # accumulate outputs
                for out_name, outvals in batch_outs.items():
                    accumulators[out_name].append(outvals)
                # on batch end triggers
                self.on_batch_end.send(self)
        except tf.errors.OutOfRangeError:
            pass
        return accumulators

    def learn_step(self, outputs):
        try:
            outputs["update_opt"] = self._update_opt
            sess = tf.get_default_session()
            ret = sess.run(
                fetches=outputs
            )
            ret.pop("update_opt")
            return ret
        finally:
            outputs.pop("update_opt")

    def fit(self):
        """
        Learning fit function. Starts the fitting procedure.
        :return:
        """
        # on train begin triggers
        self.on_train_begin.send(self)
        # main loop
        for epoch_i in range(int(self.model.config["FLOW.N_EPOCHS"])):
            self.current_state["current_epoch"] = epoch_i
            # on epoch begin trigger
            self.on_epoch_begin.send(self)

            # epoch begin trigger
            accumulators = self.epoch_fit_loop(self.outputs)
            self._aggregate_accumulators(accumulators)
            self.validate_sig.send(self)
            self.on_epoch_end.send(self)

            # print(">>>>current_state>>>", self.current_state)
            print(
                "Epoch '{i}'=> loss: {loss:0.5f}, ".format(
                    i=self.current_state["current_epoch"] + 1,
                    loss=self.current_state["loss"]
                ), self.current_state
            )

            # checks when the stop train flag is set to true
            # and break the main training loop when it happens
            if self._stop_flag:
                break

        # on train end triggers
        self.on_train_end.send(self)

    def _initialize_session(self):
        """Default session initialization function."""
        if not self.model._is_session_initialized:
            # tf global variables initialization (session variables initialization)
            # sess = tf.get_default_session()
            # sess.run(tf.global_variables_initializer())
            # self.model._is_session_initialized = True
            sess = tf.get_default_session()
            not_initialized = sess.run([tf.is_variable_initialized(var) for var in tf.global_variables()])
            not_initialized = [v for (v, f) in zip(tf.global_variables(), not_initialized) if not f]
            if len(not_initialized) > 0:
                sess.run(tf.variables_initializer(not_initialized))
            self.model._is_session_initialized = True
