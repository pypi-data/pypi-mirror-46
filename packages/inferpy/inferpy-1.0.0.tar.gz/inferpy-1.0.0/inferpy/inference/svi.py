import tensorflow as tf
import inspect
import itertools

from . import loss_functions
import inferpy as inf
from inferpy import util
from inferpy import contextmanager


class SVI:
    def __init__(self, qmodel, loss='ELBO', optimizer='AdamOptimizer', batch_size=100, epochs=1000):
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

        self.batch_size = batch_size
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
        # create a tf dataset and an iterator, specifying the batch size
        plate_size = util.iterables.get_plate_size(pmodel.vars, sample_dict)
        batches = int(plate_size / self.batch_size)  # M/N
        batch_weight = self.batch_size / plate_size  # N/M

        tfdataset = (
            tf.data.Dataset.from_tensor_slices(sample_dict)
            .shuffle(plate_size)  # use the size of the complete dataset for shuffle buffer, so we use a perfect shuffle
            .batch(self.batch_size, drop_remainder=True)  # discard the remainder batch with less elements if exists
            .repeat()
        )
        iterator = tfdataset.make_one_shot_iterator()
        input_data = iterator.get_next()  # each time this tensor is evaluated in a session it contains new data

        # Create the loss function tensor
        loss_tensor = self.loss_fn(pmodel, self.qmodel, plate_size=self.batch_size, batch_weight=batch_weight)

        train = self.optimizer.minimize(loss_tensor)

        t = []

        sess = inf.get_session()
        # Initialize all variables which are not in the probmodel p, because they have been initialized before
        model_variables = set([v for v in itertools.chain(
            pmodel.params.values(),
            (pmodel._last_expanded_params or {}).values(),
            (pmodel._last_fitted_params or {}).values(),
            self.qmodel.params.values(),
            (self.qmodel._last_expanded_params or {}).values(),
            (self.qmodel._last_fitted_params or {}).values()
            )])
        sess.run(tf.variables_initializer([v for v in tf.global_variables()
                                           if v not in model_variables and not v.name.startswith("inferpy-")]))

        for i in range(self.epochs):
            for j in range(batches):
                # evaluate the data tensor to get an evaluated one which can be used to observe varoables
                local_input_data = sess.run(input_data)
                with contextmanager.observe(pmodel._last_expanded_vars, local_input_data):
                    with contextmanager.observe(self.qmodel._last_expanded_vars, local_input_data):
                        sess.run(train)

                        t.append(sess.run(loss_tensor))
                        if i % 200 == 0:
                            print("\n {} epochs\t {}".format(i, t[-1]), end="", flush=True)
                        if i % 20 == 0:
                            print(".", end="", flush=True)

        # set the private __losses attribute for the losses property
        self.__losses = t

        return self.qmodel._last_expanded_vars, self.qmodel._last_expanded_params

    @property
    def losses(self):
        return self.__losses
