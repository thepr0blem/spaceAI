"""
--- SpaceAI game ---

The main purpose of this exercise is to build a simple "space runner" game which will be an environment
for genetic algorithm implementation.

The game has 4 modes:
A. Random Autopilot - spaceship is steered by AI with randomly initialized neural network
B. Human Player - spaceship is steered by human player (LEFT and RIGHT arrow keys)
C. Simulation - in this mode population is generated and evolved until the user decides to stop on current generation
and save latest genes of most successful pilot to file
D. Top Pilot - loads genes from previous simulations and initialize intelligent pilot to steer the spaceship

Tips for moving between screens:
- Game Over Menu is displayed after spaceship dies in modes A, B or D. From Game Over Menu user may go to Main Menu
or restart current mode.
- Simulation - press R to go to Simulation Menu. Here you can save latest genes, restart simulation or go to Main Menu

Run this file to turn on the game.

"""
import arcade
import time

from settings import *
from game_classes import Obstacle, SpaceShip, Population
from drawer import Drawer
from key_event_handler import KeyEventHandler
from collision_system import CollisionSystem


class MyGame(KeyEventHandler, CollisionSystem, Drawer, arcade.Window):
    """Game class. """

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # Mouse cursor not visible
        self.set_mouse_visible(False)

        # Background
        self.background = arcade.load_texture("images/background.png")

        # Variables initialization
        self.ship = None
        self.score = 0
        self.obstacle_list = None
        self.closest_obstacle = None
        self.AI_mode = False
        self.smart_AI_mode = False
        self.simulation_mode = False

        self.current_state = MENU

        self.population = Population()
        self.population.populate()

    def setup(self):
        """Set up the game. """

        # Create player/population
        if self.simulation_mode:
            self.population.generation_id += 1
            self.population.ressurect_ships()

        else:
            if self.smart_AI_mode:
                self.ship = SpaceShip(320, 50, 0, 15)
                self.ship.pilot.load_best_genes()

            else:
                self.ship = SpaceShip(320, 50, 0, 15)

        # Score
        self.score = 0

        # Create obstacles
        self.obstacle_list = []
        self.closest_obstacle = 0

        for i in range(NO_OBSTACLES):
            obstacle = Obstacle(SCREEN_HEIGHT + i * OBSTACLE_FREQ)
            self.obstacle_list.append(obstacle)

    def on_draw(self):
        """Called whenever we need to draw the window. """

        arcade.start_render()

        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        if self.current_state == MENU:
            self.draw_menu()

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        elif self.current_state == EVOLUTION:
            self.draw_game()
            self.draw_evo_state()

        elif self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_over(self.ship.pilot.pilot_score)

        elif self.current_state == SIMULATION_MENU:
            self.draw_game()
            self.draw_sim_menu()

    def update(self, delta_time):
        """Updates current state of the game. """

        # --- SIMULATION MODE (POPULATION OF SHIPS) --- #
        if self.simulation_mode:

            if self.current_state == EVOLUTION:
                time.sleep(0.5)
                self.population.evolve()
                self.current_state = GAME_RUNNING
                self.setup()

            elif self.current_state == GAME_RUNNING:

                self.check_for_collision()

                # Check if whole generation died
                if self.population.check_if_all_dead():

                    # Deactivate obstacles
                    for i in range(3):
                        self.obstacle_list[i].is_active = False

                    self.current_state = EVOLUTION

                # Passing obstacles
                self.pass_obstacles()

                # Population updates
                for ship in self.population.ships_list:
                    if ship.alive:
                        ship.update(ai_state=self.AI_mode,
                                    gap_x1=self.obstacle_list[self.closest_obstacle].gap_x1,
                                    gap_x2=self.obstacle_list[self.closest_obstacle].gap_x2)

                # Obstacles update
                for obstacle in self.obstacle_list:
                    obstacle.update(delta_time)

        # --- SINGLE SHIP MODE --- #
        else:
            if self.current_state == GAME_RUNNING:

                self.pass_obstacles()  # Passing obstacles

                # Ship update
                self.ship.update(ai_state=self.AI_mode,
                                 gap_x1=self.obstacle_list[self.closest_obstacle].gap_x1,
                                 gap_x2=self.obstacle_list[self.closest_obstacle].gap_x1)

                # Obstacles update
                for obstacle in self.obstacle_list:
                    obstacle.update(delta_time)

                self.check_for_collision()


def main():
    window = MyGame(640, 480, "spaceAI")
    window.set_update_rate(1/60)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
