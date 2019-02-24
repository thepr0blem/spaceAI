"""
 Game classes:
    - SpaceShip
    - Obstacle
    - Population - collection of Spaceships
    - Pilot - "brain" of SpaceShip, decides on what movement should be done by SpaceShip when in non-human player mode
"""

import random as rd
import arcade
import numpy as np

from settings import *
from ext_functions import softmax, relu, cross_over


# ------------------------------------------------------------------------------------------------------------------- #
class Population:
    """
    Collection of SpaceShip objects, which together with their pilots will be evolving as playing

    Methods:
        - populate - generates collection of POPULATION_SIZE ships
        - restart_sim - restars population by cleaning ships_list and performing fresh initialization
        - evolve - performs evolution algorithm steps: selection, crossover and mutation and reassigns Pilots genotypes
        - save_best_genes - saves genes of latest top scorer to file
        - ressurect_ships - resurrects all ships in population and reposition them to the middle of the screen
        - check_if_all_dead - returns TRUE if all ships are dead
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
        """Restart population by cleaning ships_list and performing fresh initialization. """

        self.ships_list = []
        self.dead_ships_list = []
        self.top_ships = []
        self.generation_id = 0
        self.populate()

    def ressurect_ships(self):
        """Resurrects all ships in population and reposition them to the middle of the screen. """

        for ship in self.ships_list:
            ship.alive = True
            ship.position_x = int(SCREEN_WIDTH / 2)

        self.all_dead = False

    def check_if_all_dead(self):
        """Checks if all ships are dead. """

        alive_ships_num = 0
        self.all_dead = True
        for ship in self.ships_list:
            if ship.alive:
                self.all_dead = False
                alive_ships_num += 1

        self.living_ships = alive_ships_num
        return self.all_dead

    def evolve(self):
        """Performs evolution algorithm steps: selection, crossover and mutation and reassigns Pilots genotypes. """

        # --- Selection ---
        self.dead_ships_list = self.ships_list[:]
        # Sort ships by their performance (measured by score)
        self.dead_ships_list.sort(key=lambda c: c.pilot.pilot_score, reverse=True)

        # Assign best scorers to top_ships
        self.top_ships = self.dead_ships_list[:int(SELECTION_RATE * POPULATION_SIZE)]

        # --- Evolution ---
        # Top ships are survivors, they go to next generation
        for i in range(int(SELECTION_RATE * POPULATION_SIZE)):
            self.ships_list[i] = self.top_ships[i]

        # Generate "children" for the next generation by crossing over randomly chosen parents from top_ships
        for i in range(int(SELECTION_RATE * POPULATION_SIZE), POPULATION_SIZE):

            new_gen_a, new_gen_b = cross_over(self.top_ships)

            self.ships_list[i].pilot.genotype_a = new_gen_a
            self.ships_list[i].pilot.genotype_b = new_gen_b


# ------------------------------------------------------------------------------------------------------------------- #
class Pilot:
    """Pilot (or brain) for SpaceShip class. Its genes store information on weights for nerual network that
    make a decision on next movement of the ship. """
    def __init__(self):

        # Random initialization of weights for neural network using two arrays:
        self.genotype_a = np.random.randn(NEURONS, 3)  # 1. NN Weights: INPUT -> HIDDEN LAYER
        self.genotype_b = np.random.randn(3, NEURONS)  # 2. NN Weights: HIDDEN LAYER -> OUTPUT LAYER

        self.pilot_score = 0

    def decide(self, x_ship, gap_x1, gap_x2):
        """
        Making decision on which direction ship moves using neural network.
        Properties of neural network:
            Input: x coordinates of the ship and closest obstacle (x_ship, gap_x1, gap_x2)
            Structure of NN:
            - 3 input values
            - 1 hidden layer with n neurons (n -> see NEURONS var in settings)
            - 3 output values
            Output: 0 - STAY, 1 - LEFT, 2 - RIGHT
        """

        input_lay = np.array((x_ship, gap_x1, gap_x2)).reshape(3, 1) / SCREEN_WIDTH
        hid_lay = relu(np.dot(self.genotype_a, input_lay))
        output = softmax(relu(np.dot(self.genotype_b, hid_lay)))

        return np.argmax(output)

    def load_best_genes(self):
        """Load best genes from latest saved simulation. """

        # Saved file directory defined in settings
        self.genotype_a = np.load(BEST_GEN_A_PATH)
        self.genotype_b = np.load(BEST_GEN_B_PATH)

    def save_genes(self):
        """Saves pilot's genes to file. """

        # Save to files
        np.save(BEST_GEN_A_PATH, self.genotype_a)
        np.save(BEST_GEN_B_PATH, self.genotype_b)


# ------------------------------------------------------------------------------------------------------------------- #
class SpaceShip:
    """
    Spaceship game class.

    Methods:
        - draw - draws the spaceship
        - update - updates current state of spaceship e.g. position
    """

    def __init__(self, position_x, position_y, change_x, h_width):

        # Geometrical params
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.half_width = h_width
        self.center_y = self.position_y + 20

        # In-game params
        self.alive = True
        self.pilot = Pilot()

    def draw(self):
        """Draws the spaceship. """

        if self.alive:

            arcade.draw_point(self.position_x, self.position_y + 20, arcade.color.BLACK, 5)

            texture = arcade.load_texture("images/spaceShips_008.png")
            scale = .5

            arcade.draw_texture_rectangle(self.position_x, self.position_y + 20,
                                          scale * texture.width, scale * texture.height,
                                          texture, 0)

    def update(self, ai_state, gap_x1, gap_x2):
        """Updates current status of spaceship. """

        # --- MOVEMENT ---
        # If non-human player decides on next movement
        # Rules applied: 0 - STAY, 1 - LEFT, 2 - RIGHT
        if ai_state:
            if self.pilot.decide(self.position_x, gap_x1, gap_x2) == 0:
                self.position_x += 0
            elif self.pilot.decide(self.position_x, gap_x1, gap_x2) == 1:
                self.position_x += - MOVEMENT_SPEED
            else:
                self.position_x += MOVEMENT_SPEED

        # When human player decides on next movement
        else:
            # Move left or right
            self.position_x += self.change_x

        # --- COLLISIONS WITH SCREEN EDGES ---
        if self.position_x < self.half_width:
            self.position_x = self.half_width

        if self.position_x > SCREEN_WIDTH - self.half_width:
            self.position_x = SCREEN_WIDTH - self.half_width


# ------------------------------------------------------------------------------------------------------------------- #
class Obstacle:
    """Obstacle game class.

    Methods:
    - draw - draws space obstacle
    - respawn - respawn obstacle "above" the visibile screen area after passing by the spaceship y position
    - update - updates current state of obstacle (moves obstacle down the screen)
    """
    def __init__(self, position_y):

        # --- GAP generation ---
        # left edge x_position random generation:
        self.gap_x1 = rd.randrange(0, 440, 1)
        # right edge x_position random generation to be between 100 to 200 pixels from left x_position
        self.gap_x2 = rd.randrange(self.gap_x1 + 100, self.gap_x1 + 200, 1)
        self.position_y = position_y
        self.thickness = 20
        self.color = arcade.color.ANTI_FLASH_WHITE
        self.is_active = True
        self.is_textured = True

    def draw(self):
        """Draw space obstacle. """

        # --- TEXTURED RECTANGLE ---
        if self.is_textured:
            obstacle_texture = arcade.load_texture("images/spaceBuilding_016.png")

            arcade.draw_texture_rectangle(0.5 * self.gap_x1, self.position_y,
                                          self.gap_x1, self.thickness,
                                          obstacle_texture)

            arcade.draw_texture_rectangle(0.5 * (SCREEN_WIDTH + self.gap_x2), self.position_y,
                                          SCREEN_WIDTH - self.gap_x2, self.thickness,
                                          obstacle_texture)

        # --- WHITE RECTANGLE ---
        else:
            arcade.draw_rectangle_filled(0.5 * self.gap_x1, self.position_y,
                                         self.gap_x1, self.thickness,
                                         self.color)

            arcade.draw_rectangle_filled(0.5 * (SCREEN_WIDTH + self.gap_x2), self.position_y,
                                         SCREEN_WIDTH - self.gap_x2, self.thickness,
                                         self.color)

    def update(self, delta_time):
        """Move obstacle downwards. """

        # Move the obstacle
        if self.is_active:
            self.position_y -= OBSTACLE_SPEED * delta_time

        # If obstacle "below" the screen, respawn
        if self.position_y < 0:
            self.respawn()

    def respawn(self):
        """Respawn obstacle after going out of the screen. """

        self.gap_x1 = rd.randrange(0, 440, 1)
        self.gap_x2 = rd.randrange(self.gap_x1 + 100, self.gap_x1 + 200, 1)
        self.position_y = SCREEN_HEIGHT + OBSTACLE_FREQ

# ------------------------------------------------------------------------------------------------------------------- #
