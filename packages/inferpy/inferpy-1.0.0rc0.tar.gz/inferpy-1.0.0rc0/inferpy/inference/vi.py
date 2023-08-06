import tensorflow as tf
import inspect
import itertools

from . import loss_functions
import inferpy as inf
from inferpy import util
from inferpy import contextmanager


class VI:
    def __init__(self, qmodel, loss='ELBO', optimizer='AdamOptimizer', epochs=1000):
        # store the qmodel in self.qmodel. Can be a callable with no parameters which returns the qmodel
        if callable(qmodel):
            if len(inspect.signature(qmodel).parameters) > 0:
                raise ValueError("input qmodel can only be a callable object if this does not has any input parameter")
            self.qmodel = qmodel()
        else:
            self.qmodel = qmodel

        # store the loss function in self.loss_fn
        # if it is a string, build the object automatically from loss_functions package
        if isinstance(loss, str):
            self.loss_fn = getattr(loss_functions, loss)
        else:
            self.loss_fn = loss

        self.epochs = epochs

        # store the optimizer function in self.optimizer
        # if it is a string, build a new optimizer from tf.train (default parametrization)
        if isinstance(optimizer, str):
            self.optimizer = getattr(tf.train, optimizer)()
        else:
            self.optimizer = optimizer

        # list for storing the loss evolution
        self.__losses = []

    def run(self, pmodel, sample_dict):
        # NOTE: right now we use a session in a with context, so it is open and close.
        # If we want to use consecutive inference, we need the same session to reuse the same variables.
        # In this case, the build_in_session function from RandomVariables should not be used.

        # get the plate size
        plate_size = util.iterables.get_plate_size(pmodel.vars, sample_dict)
        # Create the loss function tensor
        loss_tensor = self.loss_fn(pmodel, self.qmodel, plate_size=plate_size)

        train = self.optimizer.minimize(loss_tensor)

        t = []

        sess = inf.get_session()
        # Initialize all variables which are not in the probmodel p, because they have been initialized before
        model_variables = [v for v in itertools.chain(
            pmodel.params.values(),
            (pmodel._last_expanded_params or {}).values(),
            (pmodel._last_fitted_params or {}).values(),
            self.qmodel.params.values(),
            (self.qmodel._last_expanded_params or {}).values(),
            (self.qmodel._last_fitted_params or {}).values()
            )]

        sess.run(tf.variables_initializer([v for v in tf.global_variables()
                                           if v not in model_variables and not v.name.startswith("inferpy-")]))

        with contextmanager.observe(pmodel._last_expanded_vars, sample_dict):
            with contextmanager.observe(self.qmodel._last_expanded_vars, sample_dict):
                for i in range(self.epochs):
                    sess.run(train)

                    t.append(sess.run(loss_tensor))
                    if i % 200 == 0:
                        print("\n {} epochs\t {}".format(i, t[-1]), end="", flush=True)
                    if i % 10 == 0:
                        print(".", end="", flush=True)

        # set the private __losses attribute for the losses property
        self.__losses = t

        return self.qmodel._last_expanded_vars, self.qmodel._last_expanded_params

    @property
    def losses(self):
        return self.__losses
