'''
Some small utilities for Keras model creation & training

Paulo Villegas, 2017-2019
'''

from __future__ import division, print_function
import numpy as np


import keras
from IPython.core.display import SVG


# ----------------------------------------------------------------------


def model_thread_safe(model):
    '''
    This is needed to be able to use the Keras model in another thread (as it
    is done if wrapped by ProcessWrap)

    Tensorflow Graphs (https://www.tensorflow.org/api_docs/python/tf/Graph) are
    not thread-safe. We need to perform all create operations for a session in a
    single thread. So this has to be executed _before_ training starts.
    '''
    if keras.backend.backend() != 'tensorflow':
        return

    import tensorflow as tf

    session = tf.Session()
    keras.backend.set_session(session)

    model._make_predict_function()
    model._make_train_function()
    model._make_test_function()


# ----------------------------------------------------------------------


def _layer_label(layer, show_layer_names):
    '''Select the node label from the layer'''
    from keras.layers.wrappers import Wrapper

    layer_name = layer.name
    class_name = layer.__class__.__name__
    if isinstance(layer, Wrapper):
        layer_name = '{}({})'.format(layer_name, layer.layer.name)
        child_class_name = layer.layer.__class__.__name__
        class_name = '{}({})'.format(class_name, child_class_name)

    return '{}: {}'.format(layer_name, class_name) if show_layer_names else class_name


def model_to_dot(model,
                 show_shapes=False,
                 show_layer_names=True,
                 rankdir='TB'):
    """
    A modification of keras.utils.vis_utils. model_to_dot
     - style boxes
     - check nodes exist when defining edges, and if not create them
       (might happen with an InputLayer created automatically)
    --------------------------------------------------------------------------

    Convert a Keras model to dot format.

    # Arguments
        model: A Keras model instance.
        show_shapes: whether to display shape information.
        show_layer_names: whether to display layer names.
        rankdir: `rankdir` argument passed to PyDot,
            a string specifying the format of the plot:
            'TB' creates a vertical plot;
            'LR' creates a horizontal plot.

    # Returns
        A `pydot.Dot` instance representing the Keras model.
    """
    from keras.models import Sequential
    import pydot

    #_check_pydot()
    dot = pydot.Dot()
    dot.set('rankdir', rankdir)
    dot.set('concentrate', True)
    dot.set_node_defaults(shape='record', style='filled',
                          fillcolor='aliceblue', fontsize='10',
                          fontname='Trebuchet MS, Tahoma, Verdana, Arial, Helvetica, sans-serif')

    if isinstance(model, Sequential):
        if not model.built:
            model.build()
    layers = model.layers

    # Create graph nodes.
    for layer in layers:
        layer_id = str(id(layer))

        label = _layer_label(layer, show_layer_names)

        # Rebuild the label as a table including input/output shapes.
        if show_shapes:
            try:
                outputlabels = str(layer.output_shape)
            except AttributeError:
                outputlabels = 'multiple'
            if hasattr(layer, 'input_shape'):
                inputlabels = str(layer.input_shape)
            elif hasattr(layer, 'input_shapes'):
                inputlabels = ', '.join(
                    [str(ishape) for ishape in layer.input_shapes])
            else:
                inputlabels = 'multiple'
            label = '%s\n|{input:|output:}|{{%s}|{%s}}' % (label,
                                                           inputlabels,
                                                           outputlabels)
        node = pydot.Node(layer_id, label=label)
        dot.add_node(node)

    # Connect nodes with edges.
    for layer in layers:
        layer_id = str(id(layer))
        for i, node in enumerate(layer._inbound_nodes):
            node_key = layer.name + '_ib-' + str(i)
            if node_key in model._network_nodes:
                for inbound_layer in node.inbound_layers:
                    inbound_layer_id = str(id(inbound_layer))
                    dot.add_edge(pydot.Edge(inbound_layer_id, layer_id))
                    # Ensure the source layer exists in the graph as a node
                    if not dot.get_node(inbound_layer_id):
                        label = _layer_label(inbound_layer, show_layer_names)
                        node = pydot.Node(inbound_layer_id, label=label,
                                          style="filled, rounded",
                                          fillcolor='darkgoldenrod1')
                        dot.add_node(node)
    return dot


def model_layers_graph(model, show_shapes=True):
    '''
    Display a Keras model in a notebook by rendering it as SVG
    '''
    dot = model_to_dot(model, show_shapes=show_shapes)
    #dot.set( 'rankdir', 'LR')
    #for n in dot.get_nodes():
    #    n.set('style', 'filled')
    #    n.set('fillcolor', 'aliceblue')
    #    n.set('fontsize', '10')
    #    n.set('fontname', 'Trebuchet MS, Tahoma, Verdana, Arial, Helvetica, sans-serif')
    img = dot.create_svg()
    return SVG(data=img)


# ----------------------------------------------------------------------

def model_layers_list(model):
    '''
    List all layers in a Keras model
    '''
    print("Model layers:")
    for i, layer in enumerate(model.layers):
        print("  {:3}: {}".format(i+1, layer.name))
        #print ("      ",layer.trainable_weights,layer.non_trainable_weights)
        for n, w in zip(layer.trainable_weights, layer.get_weights()):
            print("       {}: w = {}".format(n, w.shape))


# ----------------------------------------------------------------------

def pred_show(pred, truth=None):
    '''
    Show prediction results
     :param pred (NumPy array): a set of predictions for test instances. Each
       prediction is the vector of probabilities for each output class
     :param truth (NumPy vector): the ground truth results: a vector with the
       true classes for each test instance.
    '''
    print('  n res ' if truth is None else '  n res true    ', end='     ')
    for c in range(pred.shape[1]):
        print("{:7}".format(c+1), end=' ')
    ok = 0
    for i, r in enumerate(pred):
        print('\n{:3}  {:2}'.format(i+1, np.argmax(r)+1), end=' ')
        if truth is not None:
            print("{:4}".format(truth[i]+1), end=' ')
            print("ok" if truth[i] == np.argmax(r) else "- ", end=" ")
            ok += truth[i] == np.argmax(r)
        print(' -> ', end=' ')
        for c in r:
            print("{:7.5f}".format(c), end=' ')

    print()
    if truth is not None:
        num = pred.shape[0]
        print("\ntotal: {}   ok: {}   accuracy: {:.3f}".format(num, ok, ok/num))


# ----------------------------------------------------------------------

def model_compare(m1, m2):
    '''
    Compare the weights in two models (the two models are assumed to have the
    same architecture)
    '''
    print("Comparing weights in model layers:")
    i = 0
    for l1, l2 in zip(m1.layers, m2.layers):
        print("  {:3}: {}".format(i+1, l1.name.encode('utf8')))
        assert(l1.name == l2.name)
        #print ("      ",layer.trainable_weights,layer.non_trainable_weights)
        for w1, w2 in zip(l1.get_weights(), l2.get_weights()):
            if not np.allclose(w1, w2):
                print('Not equal')
                for c1, c2 in zip(w1, w2):
                    print(c1, c2)
                return
        i += 1


# ----------------------------------------------------------------------

def wrapper_decorator(orig_update):
    """
    A decorator for the progress bar update function, so that it does
    not crash on I/O errors (assumedly due to some multithreading collision
    in ipykernel, patched in https://github.com/ipython/ipykernel/pull/123
    for ipykernel > 4.3.1)
    """
    def wrapped_update(self, current, values=[], **kwargs):
        try:
            orig_update(self, current, values, **kwargs)
        except ValueError:
            pass

    return wrapped_update


def wrapper_init(orig):
    """
    A decorator for the progress bar constructor, to increase the update interval
    to 1 sec (and thus reduce the amount of information generated)
    """
    def wrapped_init(self, target, **kwargs):
        kwargs['interval'] = 1
        orig(self, target, **kwargs)

    return wrapped_init


# Monkey-patch the constructor in the Progbar class to use 1-sec update intervals
import keras.utils.generic_utils as kgutils
kgutils.Progbar.__init__ = wrapper_init(kgutils.Progbar.__init__)

#kgutils.Progbar.update = wrapper_decorator(kgutils.Progbar.update)


# ----------------------------------------------------------------------
