import sys, os

import numpy as np
import matplotlib.pyplot as plt

import theano
import theano.tensor as T 
import lasagne

from load_dataset import *
from neuralnet import build

from deep import DeepAutoEncoder

def main():
    
    X_train, y_train, X_val, y_val, X_test, y_test = load_dataset()

    input_var = T.matrix('inputs')
    target_var = T.matrix('targets')

#    network = DeepAutoEncoder(784, [300, 2, 300]).hidden_layers[2]
#    model = 'adam_deep300-2-300_0.01'

#    network = DeepAutoEncoder(784, [300, 150, 2, 150, 300]).hidden_layers[4]
#    model = 'adam_deep_0.01'
    network = DeepAutoEncoder(784, [300, 2])
    network.finish_network()
    network = network.hidden_layers[2]
    model = 'adam_deep_test_tied'

    with np.load('models/model_%s.npz' % model) as f:
        print f.files
#        param_values = [f['arr_%d' % j] for j in range(len(f.files[:8]))]
        param_values = [f['arr_%d' % j] for j in range(len(f.files[:4]))]
        lasagne.layers.set_all_param_values(network, param_values)

    test_prediction = lasagne.layers.get_output(network, deterministic=True)

    indices = np.arange(X_test.shape[0])
    np.random.shuffle(indices)
    indices = indices[:1000]

    X, Y = X_test[indices], y_test[indices]

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'darkgreen', 'lime']
            
    out = lasagne.layers.get_output(network, X).eval()
#    tsne = sklearn.manifold.TSNE()
#    out = tsne.fit_transform(out)

    for j in np.unique(y_test):
        plt.scatter(out[Y == j][:, 0], out[Y == j][:, 1], color=colors[j], label=str(j))

    plt.legend()
    plt.show()

main()
