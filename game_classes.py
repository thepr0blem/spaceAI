""" Classes of game objects:
        SpaceShip - player class
        Obstacle - obstacle, moving walls class
"""

import random as rd
import arcade
import numpy as np

from game_settings import *
from add_functions import softmax, relu


class Population:

    """
    Concept:
      This is group of SpaceShip objects, which together with their pilots will be evolving as playing

      Initialization: If memory of population is empty initalize random Pilots,
                       else: take historical data and evolve population
      Methods:
      - evolve (mutation)
      - restart (move dead to playing)
      - save best genes to file
    """

    def __init__(self):

        self.size = None
        self.generation_id = 0
        self.ships_list = []
        self.dead_ships_list = []

    def populate(self, size=POPULATION_SIZE):

        self.size = size

        for i in range(size):

            self.ships_list.append(SpaceShip(50, 50, 0, 15, arcade.color.BLUE_GREEN))

    def cross_over(self, top_ten_ships):

        xoW = rd.random()   # cross over weight

        pilot_1 = rd.choice(top_ten_ships).pilot
        pilot_2 = rd.choice(top_ten_ships).pilot

        gen_a_new = pilot_1.genotype_a * xoW + (1 - xoW) * pilot_2.genotype_a
        gen_b_new = pilot_1.genotype_b * xoW + (1 - xoW) * pilot_2.genotype_b

        return gen_a_new, gen_b_new

    def evolve(self):

        self.generation_id += 1
        self.dead_ships_list = self.ships_list[:]
        self.dead_ships_list.sort(key=lambda c: c.points_when_died, reverse=True)

        top_ten_ships = self.dead_ships_list[:10]

        # Save the best genotype to file
        # file_a = r"./generation_logs/genotype_a_{}.npy".format(self.generation_id)
        # file_b = r"./generation_logs/genotype_b_{}.npy".format(self.generation_id)

        # np.save(file_a, top_ten_ships[0].pilot.genotype_a)
        # np.save(file_b, top_ten_ships[0].pilot.genotype_b)

        for i in range(int(0.2 * POPULATION_SIZE)):
            self.ships_list[i] = self.dead_ships_list[i]
            self.ships_list[i].alive = True

        for i in range(int(0.2 * POPULATION_SIZE), self.size):

            new_gen_a, new_gen_b = self.cross_over(top_ten_ships)

            self.ships_list[i].pilot.genotype_a = new_gen_a
            self.ships_list[i].pilot.genotype_b = new_gen_b
            self.ships_list[i].alive = True


class Pilot:
    def __init__(self):

        # Random initialization of weights for neural network using two arrays:
        # 1. Weights input -> hidden layer
        self.genotype_a = np.random.randn(8, 3)
        # 2. Weights hidden layer -> output
        self.genotype_b = np.random.randn(3, 8)

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
        hid_lay = relu(np.dot(self.genotype_a, input_lay))
        output = softmax(relu(np.dot(self.genotype_b, hid_lay)))

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

    def draw(self):
        """ Draw the spaceship with the instance variables we have. """

        if self.alive:

            # arcade.draw_triangle_filled(self.position_x, self.position_y + 40,
            #                             self.position_x - self.half_width, self.position_y,
            #                             self.position_x + self.half_width, self.position_y,
            #                             self.color)

            arcade.draw_point(self.position_x, self.position_y + 20, arcade.color.BLACK, 5)

            texture = arcade.load_texture("images/spaceShips_008.png")
            scale = .5

            arcade.draw_texture_rectangle(self.position_x, self.position_y + 20,
                                          scale * texture.width, scale * texture.height,
                                          texture, 0)

    def update(self, ai_state, gap_x1, gap_x2):

        if not ai_state:
            # Move left or right
            self.position_x += self.change_x

        if ai_state:
            if self.pilot.decide(self.position_x, gap_x1, gap_x2) == 0:
                self.position_x += 0
            elif self.pilot.decide(self.position_x, gap_x1, gap_x2) == 1:
                self.position_x += - MOVEMENT_SPEED
            else:
                self.position_x += MOVEMENT_SPEED

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
