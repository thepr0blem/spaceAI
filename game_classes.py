""" Classes of game objects:
        SpaceShip - player class
        Obstacle - obstacle, moving walls class
"""

import random as rd
import arcade
import numpy as np

from game_settings import *
from add_functions import softmax, relu


class Pilot:
    def __init__(self):

        # Random initialization of weights for neural network using two arrays:
        # 1. Weights input -> hidden layer
        # 2. Weights hidden layer -> output
        self.genotype = [np.random.randn(8, 3), np.random.randn(3, 8)]

        self.latest_score = 0   # Latest score

    def decide(self, x_ship, gap_x1, gap_x2):
        """
        Making decision on which direction ship moves using neural network.
        Properties of neural network:
            Input:
            - closest obstacle position (gap_x1, gap_x2, delta_y)
            Structure of NN:
            - 3 input values
            - 1 hidden layer with 8 neurons
            - 3 output values
            Returns: 0 - STAY, 1 - LEFT, 2 - RIGHT
        """

        input_lay = np.array((x_ship, gap_x1, gap_x2)).reshape(3, 1) / SCREEN_WIDTH
        hid_lay = relu(np.dot(self.genotype[0], input_lay))
        output = softmax(relu(np.dot(self.genotype[1], hid_lay)))

        return np.argmax(output)


class SpaceShip:
    def __init__(self, position_x, position_y, change_x, h_width, color):

        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.half_width = h_width
        self.color = color
        self.center_y = self.position_y + 20
        self.alive = True
        self.points_when_died = 0
        self.pilot = Pilot()
        self.AI = False

    def draw(self):
        """ Draw the spaceship with the instance variables we have. """

        arcade.draw_triangle_filled(self.position_x, self.position_y + 40,
                                    self.position_x - self.half_width, self.position_y,
                                    self.position_x + self.half_width, self.position_y,
                                    self.color)

        arcade.draw_point(self.position_x, self.position_y + 20, arcade.color.BLACK, 5)

    def update(self, AI_state, gap_x1, gap_x2):

        if not AI_state:
            # Move left or right
            self.position_x += self.change_x

        if AI_state:
            if self.pilot.decide(self.position_x, gap_x1, gap_x2) == 0:
                self.position_x += 0
            elif self.pilot.decide(self.position_x, gap_x1, gap_x2) == 1:
                self.position_x += - MOVEMENT_SPEED
            else: self.position_x += MOVEMENT_SPEED

        # Check for collisions with screen "edges"
        if self.position_x < self.half_width:
            self.position_x = self.half_width

        if self.position_x > SCREEN_WIDTH - self.half_width:
            self.position_x = SCREEN_WIDTH - self.half_width


class Obstacle:
    def __init__(self, position_y):

        # Take the parameters of the init function above, and create instance variables out of them.
        self.gap_x1 = rd.randrange(0, 440, 1)
        self.gap_x2 = rd.randrange(self.gap_x1 + 100, self.gap_x1 + 200, 1)
        self.position_y = position_y
        self.thickness = 20
        self.color = arcade.color.ANTI_FLASH_WHITE
        self.is_active = True

    def draw(self):
        """ Draw space obstacle. """

        arcade.draw_rectangle_filled(0.5 * self.gap_x1, self.position_y,
                                     self.gap_x1, self.thickness,
                                     self.color)

        arcade.draw_rectangle_filled(0.5 * (SCREEN_WIDTH + self.gap_x2), self.position_y,
                                     SCREEN_WIDTH - self.gap_x2, self.thickness,
                                     self.color)

    def respawn(self):
        """Respawn obstacle after going out of the screen. """

        self.gap_x1 = rd.randrange(0, 440, 1)
        self.gap_x2 = rd.randrange(self.gap_x1 + 100, self.gap_x1 + 200, 1)
        self.position_y = SCREEN_HEIGHT + OBSTACLE_FREQ

    def update(self, delta_time):
        """Move obstacle downwards. """
        # Move the obstacle
        if self.is_active:
            self.position_y -= OBSTACLE_SPEED * delta_time

        # See if the ship hit the edge of the screen. If so, change direction
        if self.position_y < 0:
            self.respawn()
