from __future__ import division
import os
import numpy as np
import h5py
import keras.backend as K
from keras.callbacks import Callback

class ReplayData(Callback):
    """Creates an instance of a Keras Callback to collect information
    about the training process, mostly the weights, and store them
    in a group of a HDF5 file, together with inputs and targets passed
    as arguments.

    It also saves the Keras model itself, as an independent HDF5 file,
    named after the group_name with '_model' appended to it.

    Parameters
    ----------
    inputs: ndarray
        An array with the inputs to be used during the training of the
        model. These inputs are going to be later used to generate
        statistics and plots.
    targets: ndarray
        An array with the targets to be used during the training of the
        model. These targets are going to be later used to generate
        statistics and plots.
    filename: String
        HDF5 filename to be used to store the collected information.
        It can be an existing file, as the data will be appended to it.
    group_name: String
        Group inside the HDF5 file where the information is to be
        saved. If the informed group name already exists, it will throw
        an exception.
    model: Keras Model, optional
        If provided, it will set the model directly to the callback
        instance and execute `on_train_begin` method to initialize
        all variables and create the corresponding group in the HDF5
        file.
        This is intended to be used for analyzing the initial conditions
        of the model without ever calling its `fit` function, where
        the callback is usually called.
    """
    def __init__(self, inputs, targets, filename, group_name, model=None):
        super(ReplayData, self).__init__()
        self.handler = h5py.File('{}'.format(filename), 'a')
        self.inputs = inputs
        self.targets = targets.reshape(len(targets), -1)
        self.filepath = os.path.split(filename)[0]
        self.filename = filename
        self.group = None
        self.group_name = group_name
        self.current_epoch = -1
        self.n_epochs = 0
        if model is not None:
            self.set_model(model)
            self.set_params({
                'epochs': 0,
                'samples': len(self.inputs),
                'batch_size': len(self.inputs),
            })
            self.group_name = group_name + '_init'
            self.on_train_begin()
            self.group_name = group_name
        return

    def _append_weights(self):
        """Appends the weights to the corresponding layer and weight sequence inside the group, for the current epoch.
        """
        for i, layer in enumerate(self.model.layers):
            layer_weights = layer.get_weights()
            for j, weights in enumerate(layer_weights):
                self.group['layer{}'.format(i)]['weights{}'.format(j)][self.current_epoch + 1] = weights

    def get_lr(self):
        optimizer = self.model.optimizer
        return K.function(inputs=[],
                          outputs=[optimizer.lr *
                                   (1. / (1. + optimizer.decay * K.cast(optimizer.iterations,
                                                                        K.dtype(optimizer.decay))))])(inputs=[])[0]

    def on_train_begin(self, logs={}):
        self.model.save(os.path.join(self.filepath, '{}_model.h5'.format(self.group_name)))
        self.n_epochs = self.params['epochs']

        self.group = self.handler.create_group(self.group_name)
        self.group.attrs['samples'] = self.params['samples']
        self.group.attrs['batch_size'] = self.params['batch_size']
        self.group.attrs['n_batches'] = (self.params['samples'] + self.params['batch_size'] - 1) // \
                                        self.params['batch_size']
        self.group.attrs['n_epochs'] = self.n_epochs
        self.group.attrs['n_layers'] = len(self.model.layers)
        try:
            # Python 2
            self.group.attrs['activation_functions'] = [layer.activation.func_name
                                                        if hasattr(layer, 'activation')
                                                        else ''
                                                        for layer in self.model.layers]
        except AttributeError:
            # Python 3
            self.group.attrs['activation_functions'] = [np.string_(layer.activation.__name__)
                                                        if hasattr(layer, 'activation')
                                                        else np.string_('')
                                                        for layer in self.model.layers]
        self.group.create_dataset('inputs', data=self.inputs)
        self.group.create_dataset('targets', data=self.targets)

        self.group.create_dataset('loss', shape=(self.n_epochs,), dtype='f')
        for metric in self.model.metrics:
            metric_name = metric
            if callable(metric):
                metric_name = metric.name if hasattr(metric, 'name') else metric.__name__
            self.group.create_dataset(metric_name, shape=(self.n_epochs,), dtype='f')

        self.group.create_dataset('lr', shape=(self.n_epochs,), dtype='f')

        for i, layer in enumerate(self.model.layers):
            layer_grp = self.group.create_group('layer{}'.format(i))
            layer_weights = layer.get_weights()
            for j, weights in enumerate(layer_weights):
                layer_grp.create_dataset('weights{}'.format(j),
                                         shape=(self.n_epochs + 1, ) + weights.shape,
                                         dtype='f')
        self._append_weights()
        return

    def on_train_end(self, logs={}):
        self.handler.close()
        return

    def on_epoch_begin(self, epoch, logs={}):
        self.current_epoch = epoch
        self.group['lr'][epoch] = self.get_lr()
        return

    def on_epoch_end(self, epoch, logs={}):
        self._append_weights()
        self.group['loss'][epoch] = logs.get('loss')
        for metric in self.model.metrics:
            metric_name = metric
            if callable(metric):
                metric_name = metric.name if hasattr(metric, 'name') else metric.__name__
            self.group[metric_name][epoch] = logs.get(metric_name, np.nan)
        return
