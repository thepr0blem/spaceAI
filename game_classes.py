"""
 Classes of game objects:
        SpaceShip - player class
        Obstacle - obstacle, moving walls class
        Population - ?
        Pilot - ?
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

        # Population parameters
        self.generation_id = 0
        self.all_dead = False
        self.living_ships = POPULATION_SIZE

        # Population ship lists
        self.ships_list = []
        self.dead_ships_list = []
        self.top_ships = []

    def populate(self):
        """Generate population with ships and randomly intialized brains/pilots. """

        self.living_ships = POPULATION_SIZE
        for i in range(POPULATION_SIZE):
            self.ships_list.append(SpaceShip(320, 50, 0, 15))

    def restart_sim(self):
        """Restart population by cleaning ships_list and fresh initialization. """

        self.ships_list = []
        self.dead_ships_list = []
        self.top_ships = []
        self.generation_id = 0
        self.populate()

    def cross_over(self):
        """Generate new genoms based on randomly selected ships from n top players from previous generaiton. """

        # Crossover
        xoW = rd.random()   # cross over weight

        pilot_1 = rd.choice(self.top_ships).pilot
        pilot_2 = rd.choice(self.top_ships).pilot

        gen_a_new = pilot_1.genotype_a * xoW + (1 - xoW) * pilot_2.genotype_a
        gen_b_new = pilot_1.genotype_b * xoW + (1 - xoW) * pilot_2.genotype_b

        # Mutation
        mutationW = rd.uniform(1 - MUTATION_SCALE, 1 + MUTATION_SCALE)
        mutation = rd.random()

        if mutation <= MUTATION_PROB:
            # rd_row_a = rd.randint(0, 7)
            # rd_row_b = rd.randint(0, 2)
            #
            # gen_a_new[rd_row_a] = gen_a_new[rd_row_a] * mutationW
            # gen_b_new[rd_row_b] = gen_b_new[rd_row_b] * mutationW

            gen_a_new = gen_a_new * mutationW
            gen_b_new = gen_b_new * mutationW

        return gen_a_new, gen_b_new

    def evolve(self):
        """ DESCRIPTION """

        # Selection
        self.dead_ships_list = self.ships_list[:]
        self.dead_ships_list.sort(key=lambda c: c.points_when_died, reverse=True)

        self.top_ships = self.dead_ships_list[:int(SELECTION_RATE * POPULATION_SIZE)]

        # Taking the best from previous generation
        for i in range(int(SELECTION_RATE * POPULATION_SIZE)):
            self.ships_list[i] = self.top_ships[i]

        # Evolve
        for i in range(int(SELECTION_RATE * POPULATION_SIZE), POPULATION_SIZE):

            new_gen_a, new_gen_b = self.cross_over()

            self.ships_list[i].pilot.genotype_a = new_gen_a
            self.ships_list[i].pilot.genotype_b = new_gen_b

    def save_best_genes(self):
        """ DESCRIPTION """

        top_gen_a = self.top_ships[0].pilot.genotype_a
        top_gen_b = self.top_ships[0].pilot.genotype_b

        file_a = BEST_GEN_A_PATH
        file_b = BEST_GEN_B_PATH
        file_c = r"./generation_logs/gen_no_{}.npy".format(self.generation_id)

        np.save(file_a, top_gen_a)
        np.save(file_b, top_gen_b)
        np.save(file_c, np.zeros((1, 1)))

    def ressurect_ships(self):
        """ DESCRIPTION """

        for ship in self.ships_list:
            ship.alive = True
            ship.position_x = 320

        self.all_dead = False

    def check_if_all_dead(self):
        """ DESCRIPTION """

        live_ships_num = 0
        self.all_dead = True
        for ship in self.ships_list:
            if ship.alive:
                self.all_dead = False
                live_ships_num += 1

        self.living_ships = live_ships_num
        return self.all_dead


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

    def load_best_genes(self):
        """Load best genes from latest saved simulation. """

        loaded_gen_a = np.load(BEST_GEN_A_PATH)
        loaded_gen_b = np.load(BEST_GEN_B_PATH)

        self.genotype_a = loaded_gen_a
        self.genotype_b = loaded_gen_b


class SpaceShip:

    def __init__(self, position_x, position_y, change_x, h_width):

        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.half_width = h_width
        self.center_y = self.position_y + 20
        self.alive = True
        self.points_when_died = 0
        self.pilot = Pilot()

    def draw(self):
        """ Draw the spaceship with the instance variables we have. """

        if self.alive:

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

        # TODO: Define new texture for obstacle

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
