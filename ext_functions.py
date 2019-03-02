"""
Helper functions used in neural network implementation and evolving of population
"""
import numpy as np
import random as rd
from settings import *


def softmax(x):
    """
    Computes softmax values for each sets of scores in x.
    Input: x - list of n numbers
    Returns: Numpy array with softmax distribution and n elements
    """
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


def relu(x):
    """Activation function - Rectified Linear Unit. """
    return np.maximum(0.0, x)


def add_score(x, stay_frac):
    """
    - Calculates additional score for "stay" decisions being a certain fraction of all decisions made by the pilot.
    - Helps pilots to evolve to a state when they do not make unneccessary movements when going straight.
    """

    if 0 < x <= stay_frac:
        return (1/stay_frac) * x
    elif 1 >= x > stay_frac:
        return -(1/(1-stay_frac)) * x + 1/(1-stay_frac)
    elif x > 1 or x <= 0:
        return 0


def cross_over(pilot_1, pilot_2):
    """
    Cross genoms of two pilots to produce child genes using the following formula:
    new = parent_1 * random + parent_2 * (1 - random), where random is number in range 0-1
    """

    # --- Crossover ---
    xoW = rd.random()  # Crossover weight

    # Crossing genes of parents
    gen_a_new = pilot_1.genotype_a * xoW + (1 - xoW) * pilot_2.genotype_a
    gen_b_new = pilot_1.genotype_b * xoW + (1 - xoW) * pilot_2.genotype_b
    bias_a_new = pilot_1.bias_a * xoW + (1 - xoW) * pilot_2.bias_a
    bias_b_new = pilot_1.bias_b * xoW + (1 - xoW) * pilot_2.bias_b

    return gen_a_new, gen_b_new, bias_a_new, bias_b_new


def mutate(gen_a_new, gen_b_new, bias_a_new, bias_b_new):
    """
    Mutates genes by replacing with random numbers with probability of MUTATION_PROB (modified in settings.py)
    """

    mutation = rd.random()
    # Check if mutation happens
    if mutation <= MUTATION_PROB:

        # Modify whole genes by multiplying their weights with mutation weight
        gen_a_new = np.random.randn(NEURONS, 3)
        gen_b_new = np.random.randn(3, NEURONS)
        bias_a_new = np.random.randn(NEURONS, 1) * 0.5
        bias_b_new = np.random.randn(3, 1) * 0.5

    return gen_a_new, gen_b_new, bias_a_new, bias_b_new
