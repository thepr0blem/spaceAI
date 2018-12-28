import numpy as np


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def relu(x):
    """Activation function - ReLu."""
    return np.maximum(0.0, x)
