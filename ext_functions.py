"""Helper functions for neural network implementation. """
import numpy as np
import random as rd
from settings import *


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


def cross_over(top_ships):
    """Generate new genoms based on randomly selected ships from n top players from previous generation.

    - cross_over - generate new genotypes based on randomly selected ships from
        n [POPULATION_SIZE * SELECTION_RATE (see settings)] top players from previous generation.
        This method applies mutation and crossover steps from evolution algorithm
    """

    # --- Crossover ---
    xoW = rd.random()  # Crossover weight

    # Random choice of two pilots from top ones to take them as parents
    pilot_1 = rd.choice(top_ships).pilot
    pilot_2 = rd.choice(top_ships).pilot

    # Crossing genes of parents
    gen_a_new = pilot_1.genotype_a * xoW + (1 - xoW) * pilot_2.genotype_a
    gen_b_new = pilot_1.genotype_b * xoW + (1 - xoW) * pilot_2.genotype_b

    # --- Mutation ---
    # Random choice of mutation weight from range (typically 0.8 - 1.2)
    mutationW = rd.uniform(1 - MUTATION_SCALE, 1 + MUTATION_SCALE)

    mutation = rd.random()
    # Check if mutation happens
    if mutation <= MUTATION_PROB:

        # Modify whole genes by multiplying their weights with mutation weight
        gen_a_new = gen_a_new * mutationW
        gen_b_new = gen_b_new * mutationW

    return gen_a_new, gen_b_new
