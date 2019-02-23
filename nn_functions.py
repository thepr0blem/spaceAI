"""Helper functions for neural network implementation. """
import numpy as np


def softmax(x):
    """
    Compute softmax values for each sets of scores in x.
    Input: x - list of n numbers
    Returns: Numpy array with softmax distribution and n elements
    """
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def relu(x):
    """Activation function - Rectified Linear Unit. """
    return np.maximum(0.0, x)
