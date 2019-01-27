"""
Main script for Space-Traveler game
"""
import arcade
import time

from game_settings import *
from game_classes import Obstacle, SpaceShip, Population


class MyGame(arcade.Window):

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

    def draw_menu(self):
        """Draw MENU. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("Choose game mode: ", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 75,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("A. Random Autopilot", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 25,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("B. Human Player", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 25,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("C. Simulation", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 75,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("D. Top Pilot", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 125,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")

    def draw_game_over(self):
        """Draw "Game over" across the screen. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("Game Over", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 60,
                         arcade.color.WHITE, 54, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("1. SPACE to restart", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("2. ENTER to return to MENU", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 40,
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        if not self.simulation_mode:
            arcade.draw_text(f"Score: {self.ship.points_when_died}",
                             int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 80,
                             arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")

    def draw_evo_state(self):
        """Draw evolution loading screen. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("Evolution", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                         arcade.color.WHITE, 54, align="center", anchor_x="center", anchor_y="center")

    def draw_sim_menu(self):
        """Draw simulation menu on the screen. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("SIM MENU", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 60,
                         arcade.color.WHITE, 54, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("1. SPACE to restart simulation", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("2. S to save best genes from latest generation", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 40,
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("3. Click ESC to leave to MAIN menu", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 80,
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")

    def draw_game(self):
        """Draw ship and obstacles. """

        if self.simulation_mode:
            for ship in self.population.ships_list:
                ship.draw()
        else:
            self.ship.draw()

        for obstacle in self.obstacle_list:
            obstacle.draw()

        self.draw_bottom_bar()

    def draw_bottom_bar(self):
        """Draws bottom bar with score and closest obstacle information. """

        # Drawing bottom screen area with score and dist to closest obstacle.
        arcade.draw_rectangle_filled(320, 15, 640, 30, arcade.color.BLACK)
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.color.WHITE, 13)

        # Generation ID
        if self.simulation_mode:
            gen_id = f"gen_id: {self.population.generation_id}"
            arcade.draw_text(gen_id, 90, 10, arcade.color.WHITE, 13)

            gen_id = f"live_ships: {self.population.living_ships}"
            arcade.draw_text(gen_id, 180, 10, arcade.color.WHITE, 13)

        else:
            # Display x1 and x2 coordinates of gap in closest obstacle
            near_obs_x1 = f"gap_x1 = {round(self.obstacle_list[self.closest_obstacle].gap_x1)}"
            arcade.draw_text(near_obs_x1, 330, 10, arcade.color.WHITE, 13)

            near_obs_x1 = f"gap_x2 = {round(self.obstacle_list[self.closest_obstacle].gap_x2)}"
            arcade.draw_text(near_obs_x1, 450, 10, arcade.color.WHITE, 13)

            # Distance to closest objects (delta y)
            near_obs_y = f"Closest obstacle: delta_y = " \
                f"{int(round(self.obstacle_list[self.closest_obstacle].position_y - 70, -1))}"
            arcade.draw_text(near_obs_y, 90, 10, arcade.color.WHITE, 13)

    def check_for_collision(self):
        """Checks for collision between ship/ships and closest obstacle. """

        # Identyfing closes obstacle
        closest_obstacle_bottom_edge = self.obstacle_list[self.closest_obstacle].position_y \
                                       - self.obstacle_list[self.closest_obstacle].thickness * 0.5

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

    def on_draw(self):
        """ Called whenever we need to draw the window. """

        arcade.start_render()

        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        if self.current_state == MENU:
            self.draw_menu()

        if self.current_state == GAME_RUNNING:
            self.draw_game()

        if self.current_state == EVOLUTION:
            self.draw_game()
            self.draw_evo_state()

        if self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()

        if self.current_state == SIMULATION_MENU:
            self.draw_game()
            self.draw_sim_menu()

    def ident_clos_obstacle(self):
        """Identifies closest obstacle. """

        if self.obstacle_list[self.closest_obstacle].position_y < 70:
            if self.closest_obstacle == 3:
                self.closest_obstacle = 0
            else:
                self.closest_obstacle += 1

    def update(self, delta_time):

        # --- SIMULATION MODE (MULTIPLE SHIPS) ---
        if self.simulation_mode:

            if self.current_state == EVOLUTION:
                time.sleep(0.5)
                self.population.evolve()
                self.current_state = GAME_RUNNING
                self.setup()

            if self.current_state == GAME_RUNNING:
                self.check_for_collision()

                # Check to start evolution
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

        # --- SINGLE SHIP MODE ---
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
        """ Called whenever the user presses a key. """

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

        # --- SIMULATION MENU BUTTONS --- #
        if self.current_state == SIMULATION_MENU:
            if key == arcade.key.S:
                self.population.save_best_genes()
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


def main():
    window = MyGame(640, 480, "spaceAI")
    window.set_update_rate(1/60)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
