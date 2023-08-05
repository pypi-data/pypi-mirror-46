"""
Utilities for Keras models I/O
Paulo Villegas, 2017-2019

Definition of two functions, model_save() and model_load(), that can save a
Keras model and also its associated training history
"""

import os.path
import numpy as np

from keras.models import load_model
from keras import backend as K
import h5py


# --------------------------------------------------------------------------

def save_weights(model, basename):
    """
    *LEGACY*
    Modification of keras.engine.topology.Container.save_weights to avoid
    saving empty weights

    Keras native save_weights & load_weights methods choke on empty weights, since
    the h5py library can't load/save empty attributes (fixed in master, not yet in
    release 2.6). These functions solve the problem by skipping weight management
    in layers with no weights (e.g. an Activation or MaxPool layer)
    """
    try:
        f = h5py.File(basename+'.w.h5', 'w')

        if hasattr(model, 'flattened_layers'):
            # support for legacy Sequential/Merge behavior
            flattened_layers = model.flattened_layers
        else:
            flattened_layers = model.layers

        f.attrs['layer_names'] = [layer.name.encode('utf8') for layer in flattened_layers]

        for layer in flattened_layers:
            g = f.create_group(layer.name)
            symbolic_weights = layer.trainable_weights + layer.non_trainable_weights
            weight_values = K.batch_get_value(symbolic_weights)
            weight_names = []
            for i, (w, val) in enumerate(zip(symbolic_weights, weight_values)):
                if hasattr(w, 'name') and w.name:
                    name = str(w.name)
                else:
                    name = 'param_' + str(i)
                weight_names.append(name.encode('utf8'))
            # only add weights attribute if nonempty
            if weight_names:
                g.attrs['weight_names'] = weight_names 
            #else:
            #    g.attrs.if weight_names else np.zeros( (0,), 'S8' ) # ['']
            for name, val in zip(weight_names, weight_values):
                param_dset = g.create_dataset(name, val.shape,
                                              dtype=val.dtype)
                param_dset[:] = val
                #print( weight_names,"=", weight_values)
        f.flush()
    finally:
        f.close()


def load_weights(model, filepath):
    """
    *LEGACY*
    Modification of keras.engine.topology.Container.load_weights to check
    layer weights presence before accessing
    """
    f = h5py.File(filepath, mode='r')

    if hasattr(model, 'flattened_layers'):
        # support for legacy Sequential/Merge behavior
        flattened_layers = model.flattened_layers
    else:
        flattened_layers = model.layers

    if 'nb_layers' in f.attrs:
        # legacy format
        nb_layers = f.attrs['nb_layers']
        if nb_layers != len(flattened_layers):
            raise Exception('You are trying to load a weight file '
                            'containing ' + str(nb_layers) +
                            ' layers into a model with ' +
                            str(len(flattened_layers)) + '.')

        for k in range(nb_layers):
            g = f['layer_{}'.format(k)]
            weights = [g['param_{}'.format(p)] for p in range(g.attrs['nb_params'])]
            flattened_layers[k].set_weights(weights)
    else:
        # new file format
        layer_names = [n.decode('utf8') for n in f.attrs['layer_names']]
        if len(layer_names) != len(flattened_layers):
            raise Exception('You are trying to load a weight file '
                            'containing ' + str(len(layer_names)) +
                            ' layers into a model with ' +
                            str(len(flattened_layers)) + ' layers.')

        # we batch weight value assignments in a single backend call
        # which provides a speedup in TensorFlow.
        weight_value_tuples = []
        for k, name in enumerate(layer_names):
            g = f[name]
            if 'weight_names' not in g.attrs:
                continue        # skip layer if it has no weights
            weight_names = [n.decode('utf8') for n in g.attrs['weight_names']]
            if len(weight_names):
                weight_values = [g[weight_name] for weight_name in weight_names]
                layer = flattened_layers[k]
                symbolic_weights = layer.trainable_weights + layer.non_trainable_weights
                if len(weight_values) != len(symbolic_weights):
                    raise Exception('Layer #' + str(k) +
                                    ' (named "' + layer.name +
                                    '" in the current model) was found to '
                                    'correspond to layer ' + name +
                                    ' in the save file. '
                                    'However the new layer ' + layer.name +
                                    ' expects ' + str(len(symbolic_weights)) +
                                    ' weights, but the saved weights have ' +
                                    str(len(weight_values)) +
                                    ' elements.')
                weight_value_tuples += zip(symbolic_weights, weight_values)
        K.batch_set_value(weight_value_tuples)
    f.close()


# --------------------------------------------------------------------------

from keras.callbacks import Callback, History
from collections import defaultdict
import time

clock = getattr(time, 'perf_time', time.clock)

class TrainingHistory(Callback):
    '''
    A Keras callback class that tracks all evaluation metrics,
    both across mini-batches (history_batch) and across epochs (history_epoch)
    '''

    def on_train_begin(self, logs={}):
        self.history_batch = defaultdict(list)
        self.history_epoch = defaultdict(list)

    def on_epoch_begin(self, epoch, logs={}):
        # Start to mesure time; initialize storage for batch metrics
        self.epoch_start = clock()
        self.batches = defaultdict(list)

    def on_batch_end(self, batch, logs={}):
        # Store batch metrics
        for k in self.params['metrics']:
            if k in logs:
                self.batches[k].append(logs[k])

    def on_epoch_end(self, epoch, logs={}):
        # Store epoch metrics
        for k in self.params['metrics']:
            if k in logs:
                self.history_epoch[k].append(logs[k])
        self.history_epoch['time'].append(clock() - self.epoch_start)
        # Consolidate batch metrics
        for k, v in self.batches.items():
            self.history_batch[k].append(np.array(v))
        del self.batches

    def on_train_end(self, logs={}):
        # Create the mini-batch metric array dictionary
        self.history_batch = {k: np.array(v)
                              for k, v in self.history_batch.items()}

    @property
    def history(self):
        '''Alias for compatibility with the Keras History callback'''
        return self.history_epoch

# --------------------------------------------------------------------------


def history_load(name):
    '''
    Load a TrainingHistory object from an HDF5 file
    '''
    if not name.endswith('.h5'):
        name += '.h5'
    f = h5py.File(name, 'r')
    H = type('TrainingHistory', (object,),
             {'history': property(lambda s: s.history_epoch)})
    h = H()
    try:
        # Load params
        h.params = {}
        g = f['params']
        for k, v in g.attrs.items():
            # convert an NumPy string array into a list of str
            if isinstance(v, np.ndarray) and v.dtype.char == 'S':
                v = [s.decode('utf-8') for s in v]
            h.params[k] = v
        # Load epoch metrics
        g = f['history/epoch']
        h.history_epoch = {k: np.copy(v) for k, v in g.items()}
        # Load batch metrics
        if 'history/batch' in f:
            g = f['history/batch']
            h.history_batch = {k: np.copy(v) for k, v in g.items()}
        else:
            h.history_batch = None
    finally:
        f.close()
    return h


def history_save(history, name, verbose=True):
    '''
    Save either a TrainingHistory object, or a plain Keras History object,
    into an HDF5 file
    It stores:
     * params
     * history_epoch
     * history_batch (for TrainingHistory)
    '''
    if not name.endswith('.h5'):
        name += '.h5'
    if verbose:
        print('Saving training history ({}) into:'.format(type(history).__name__),
              name)
    f = h5py.File(name, 'w')
    try:
        # Save params
        g = f.create_group('params')
        for k, v in history.params.items():
            # check a list of strings -- possible errors in H5 (no unicode support)
            # see https://github.com/h5py/h5py/issues/441
            if isinstance(v, list):
                v = [e.encode('utf-8') if isinstance(e, str) else e for e in v]
            g.attrs[k] = v
        # Save epoch metrics
        g = f.create_group('history/epoch')
        for n, m in history.history.items():
            g.create_dataset(n, data=np.array(m))
        # Save batch metrics
        if hasattr(history, 'history_batch'):
            g = f.create_group('history/batch')
            for n, m in history.history_batch.items():
                g.create_dataset(n, data=np.array(m))
        f.flush()
    finally:
        f.close()


# --------------------------------------------------------------------------

def model_save_old(model, basename, history=None):
    """
    *LEGACY* Save a full model: architecture and weights, into a file
      @param model (Model): the Keras model to save
      @param basename (str): filename to use. Two files will be written: a
        JSON file (model architecture) and an HDF5 file (model weights)
      @param history (History): optional training history to save, as a third file
    """
    with open(basename+'.m.json', 'w') as f:
        f.write(model.to_json())
    save_weights(model, basename)
    if history:
        history_save(history, basename + '.h')


def model_load_old(basename, compile={}, history=True):
    """
    *LEGACY* Load a model saved with model_save_old(): structure & weights will be
    restored, and the model will be compiled with the passed arguments
      @param basename (str): basename used to save it
      @param compile (dict): arguments to be used when compiling the model
      @param history (bool): load also training history, if available
    """
    from keras.models import model_from_json
    model = model_from_json(open(basename+'.m.json').read())
    model.compile(**compile)
    load_weights(model, basename+'.w.h5')
    if not history:
        return model
    elif not os.path.exists(basename + '.h.h5'):
        return model, None
    return model, history_load(basename + '.h')


# --------------------------------------------------------------------------

def model_save(model, basename, verbose=True):
    """
    Save a full model (architecture and weights) into a file, plus its history
    into another file.
      @param model (Model or History): the Keras model to save, or a History
       callback object (which also contains the model)
      @param basename (str): basename to use.
    """
    if basename.endswith('.h5'):
        basename = basename[:-3]
    if isinstance(model, (History, TrainingHistory)):
        if verbose:
            print('Saving Keras model into:', basename+'.h5')
        model.model.save(basename+'.h5')
        history_save(model, basename + '.h', verbose)
    else:
        model.save(basename+'.h5')


def model_load(basename, history=True):
    """
    Load a model saved with model_save(): structure & weights will be
    restored, and the model will be re-compiled
      @param basename (str): basename used to save it
      @param history (bool): load also training history, if available
    """
    if basename.endswith('.h5'):
        basename = basename[:-3]
    model = load_model(basename + '.h5')
    if not history:
        return model
    elif not os.path.exists(basename + '.h.h5'):
        return model, None

    history = history_load(basename + '.h')
    history.model = model
    return model, history
