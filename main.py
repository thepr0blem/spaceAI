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
from draw_functions import draw_menu, draw_game_over, draw_evo_state, draw_sim_menu, draw_bottom_bar


class MyGame(arcade.Window):
    """Game class. """

    def __init__(self, width, height, title):

        # Call the parent class's init function
        super().__init__(width, height, title)

        # Mouse cursor not visible
        self.set_mouse_visible(False)

        # Background color
        arcade.set_background_color(arcade.color.CHARLESTON_GREEN)
        self.background = None

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

        # Background
        self.background = arcade.load_texture("images/background.png")

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

    def draw_game(self):
        """Draws game on the screen, including:
            -   ship / population of ships
            -   obstacles
            -   bottom bar with information
        """

        if self.simulation_mode:
            for ship in self.population.ships_list:
                ship.draw()
        else:
            self.ship.draw()

        for obstacle in self.obstacle_list:
            obstacle.draw()

        draw_bottom_bar(score=self.score,
                        simulation_mode=self.simulation_mode,
                        gen_id=self.population.generation_id,
                        living_ships=self.population.living_ships,
                        gap_x1=self.obstacle_list[self.closest_obstacle].gap_x1,
                        gap_x2=self.obstacle_list[self.closest_obstacle].gap_x2,
                        pos_y=self.obstacle_list[self.closest_obstacle].position_y)

    def on_draw(self):
        """Called whenever we need to draw the window. """

        arcade.start_render()

        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        if self.current_state == MENU:
            draw_menu()

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        elif self.current_state == EVOLUTION:
            self.draw_game()
            draw_evo_state()

        elif self.current_state == GAME_OVER:
            self.draw_game()
            draw_game_over(self.ship.points_when_died)

        elif self.current_state == SIMULATION_MENU:
            self.draw_game()
            draw_sim_menu()

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
                prev_obst = self.closest_obstacle   # passed obstacle
                self.ident_clos_obstacle()          # identifying new obstacle
                curr_obst = self.closest_obstacle   # assigning new obstacle
                if not prev_obst == curr_obst:      # if obstacle changed, add +1 point
                    self.score += 1

                # Population updates
                for ship in self.population.ships_list:
                    if ship.alive:
                        ship.update(ai_state=self.AI_mode,
                                    gap_x1=self.obstacle_list[self.closest_obstacle].gap_x1,
                                    gap_x2=self.obstacle_list[self.closest_obstacle].gap_x1)

                # Obstacles update
                for obstacle in self.obstacle_list:
                    obstacle.update(delta_time)

        # --- SINGLE SHIP MODE --- #
        else:
            if self.current_state == GAME_RUNNING:

                # Passing obstacles
                prev_obst = self.closest_obstacle   # passed obstacle
                self.ident_clos_obstacle()          # identifying new obstacle
                curr_obst = self.closest_obstacle   # assigning new obstacle
                if not prev_obst == curr_obst:      # if obstacle changed, add +1 point
                    self.score += 1

                # Ship update
                self.ship.update(ai_state=self.AI_mode,
                                 gap_x1=self.obstacle_list[self.closest_obstacle].gap_x1,
                                 gap_x2=self.obstacle_list[self.closest_obstacle].gap_x1)

                # Obstacles update
                for obstacle in self.obstacle_list:
                    obstacle.update(delta_time)

                self.check_for_collision()

    def on_key_press(self, key, modifiers):
        """Called whenever the user presses a key. """

        # --- MAIN MENU BUTTONS --- #
        if self.current_state == MENU:
            if key == arcade.key.A:
                self.current_state = GAME_RUNNING
                self.AI_mode = True
                self.simulation_mode = False
                self.smart_AI_mode = False
                self.setup()
            if key == arcade.key.B:
                self.current_state = GAME_RUNNING
                self.AI_mode = False
                self.simulation_mode = False
                self.smart_AI_mode = False
                self.setup()
            if key == arcade.key.C:
                self.current_state = GAME_RUNNING
                self.AI_mode = True
                self.simulation_mode = True
                self.smart_AI_mode = False
                self.setup()
                self.population.restart_sim()
            if key == arcade.key.D:
                self.current_state = GAME_RUNNING
                self.AI_mode = True
                self.simulation_mode = False
                self.smart_AI_mode = True
                self.setup()

        # --- GAME RUNNING BUTTONS --- #
        if self.current_state == GAME_RUNNING:

            # --- SIMULATION MODE (MULTIPLE SHIPS) ---
            if self.simulation_mode:
                if key == arcade.key.R:
                    self.current_state = SIMULATION_MENU

            # --- SINGLE SHIP MODE ---
            else:
                if self.ship.alive:
                    if not self.AI_mode:
                        if key == arcade.key.LEFT:
                            self.ship.change_x = -MOVEMENT_SPEED
                        elif key == arcade.key.RIGHT:
                            self.ship.change_x = MOVEMENT_SPEED
                    else:
                        if key == arcade.key.ESCAPE:
                            self.current_state = MENU

        # --- SIMULATION MENU BUTTONS --- #
        if self.current_state == SIMULATION_MENU:
            if key == arcade.key.S:
                self.population.top_ships[0].pilot.save_genes(gen_id=self.population.generation_id)
                self.current_state = MENU
            elif key == arcade.key.SPACE:
                self.current_state = GAME_RUNNING
                self.population.restart_sim()
            elif key == arcade.key.ESCAPE:
                self.current_state = MENU

        # --- GAME OVER BUTTONS --- #
        if self.current_state == GAME_OVER:
            if key == arcade.key.SPACE:
                self.setup()
                self.current_state = GAME_RUNNING

            if key == arcade.key.ENTER:
                self.setup()
                self.current_state = MENU

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """

        if not self.simulation_mode:
            if self.ship.alive:
                if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                    self.ship.change_x = 0

    def check_for_collision(self):
        """Checks for collision between ship / population of ships and closest obstacle. """

        # Calculating y position of closest obstacle bottom edge
        closest_obstacle_bottom_edge = self.obstacle_list[self.closest_obstacle].position_y \
                                       - self.obstacle_list[self.closest_obstacle].thickness * 0.5

        # Calculating x1, x2 positions of gap in closest obstacle
        closest_obstacle_x1 = self.obstacle_list[self.closest_obstacle].gap_x1
        closest_obstacle_x2 = self.obstacle_list[self.closest_obstacle].gap_x2

        # --- COLLISIONS IN SINGLE SHIP MODE ---
        if not self.simulation_mode:

            if 0 <= self.ship.position_x <= closest_obstacle_x1 or closest_obstacle_x2 <= self.ship.position_x <= 640:
                if self.ship.center_y >= closest_obstacle_bottom_edge:

                    self.ship.alive = False
                    self.current_state = GAME_OVER
                    self.ship.points_when_died = self.score
                    for obstacle in self.obstacle_list:
                        obstacle.is_active = False

        # --- COLLISONS IN SIMULATION MODE (MULTIPLE SHIPS) ---
        else:
            for ship in self.population.ships_list:
                if ship.alive:
                    if 0 <= ship.position_x <= closest_obstacle_x1 or closest_obstacle_x2 <= ship.position_x <= 640:
                        if ship.center_y >= closest_obstacle_bottom_edge:
                            ship.alive = False
                            ship.points_when_died = self.score

    def ident_clos_obstacle(self):
        """Identifies closest obstacle. """

        # Take the next obstacle form the list if y position of the current closest obstacle is smaller
        # than y position of center of the ship
        if self.obstacle_list[self.closest_obstacle].position_y < 70:
            if self.closest_obstacle == 3:
                self.closest_obstacle = 0
            else:
                self.closest_obstacle += 1

def main():
    window = MyGame(640, 480, "spaceAI")
    window.set_update_rate(1/60)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
