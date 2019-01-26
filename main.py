"""
Main script for Space-Traveler game
"""
import arcade
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

        # Variables initialization
        self.ship = None
        self.population = None

        self.game_over = False
        self.score = 0

        self.obstacle_list = None
        self.closest_obstacle = None

        self.current_state = MENU

        self.AI_mode = False
        self.simulation_mode = False
        self.count_dead = 0

    def setup(self):
        """Set up the game and initialize the variables. """

        if self.simulation_mode:
            # Create Population object and populate
            self.population = Population()
            self.population.populate()

        else:
            # Create player
            self.ship = SpaceShip(50, 50, 0, 15, arcade.color.BLUE_GREEN)

        self.game_over = False
        self.score = 0

        # Create obstacles
        self.obstacle_list = []
        self.closest_obstacle = 0

        for i in range(NO_OBSTACLES):

            obstacle = Obstacle(SCREEN_HEIGHT + i * OBSTACLE_FREQ)

            self.obstacle_list.append(obstacle)

    def draw_menu(self):
        """Draw "MENU"."""

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 400, 300, arcade.color.BLACK)
        arcade.draw_text("Choose game mode: ", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 50,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("A. Autopilot", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("B. Player", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 50,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("C. Simulation", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 100,
                         arcade.color.WHITE, 24, align="center", anchor_x="center", anchor_y="center")

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 400, 250, arcade.color.BLACK)
        arcade.draw_text("Game Over", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 60,
                         arcade.color.WHITE, 54, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("Click SPACE to restart", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("Click ENTER to return to MENU", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 40,
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        if not self.simulation_mode:
            arcade.draw_text(f"Score: {self.ship.points_when_died}",
                             int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 80,
                             arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")

    def draw_game(self):
        """
        Draw ship and obstacles.
        """

        if self.simulation_mode:
            for ship in self.population.ships_list:
                ship.draw()
        else:
            self.ship.draw()

        for obstacle in self.obstacle_list:
            obstacle.draw()

        self.draw_bottom_bar()

    def draw_bottom_bar(self):
        """
        Draws bottom bar with score and closest obstacle information.
        """
        # Drawing bottom screen area with score and dist to closest obstacle.
        arcade.draw_rectangle_filled(320, 15, 640, 30, arcade.color.BLACK)
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.color.WHITE, 13)

        # Generation ID
        if self.simulation_mode:
            gen_id = f"gen_id: {self.population.generation_id}"
            arcade.draw_text(gen_id, 90, 10, arcade.color.WHITE, 13)

            count_dead = f"count_dead: {self.count_dead}"
            arcade.draw_text(count_dead, 250, 10, arcade.color.WHITE, 13)

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

        closest_obstacle_bottom_edge = self.obstacle_list[self.closest_obstacle].position_y \
                                       - self.obstacle_list[self.closest_obstacle].thickness * 0.5

        closest_obstacle_x1 = self.obstacle_list[self.closest_obstacle].gap_x1
        closest_obstacle_x2 = self.obstacle_list[self.closest_obstacle].gap_x2

        # --- SINGLE SHIP MODE ---
        if not self.simulation_mode:

            if 0 <= self.ship.position_x <= closest_obstacle_x1 or closest_obstacle_x2 <= self.ship.position_x <= 640:
                if self.ship.center_y >= closest_obstacle_bottom_edge:

                    self.ship.alive = False
                    self.current_state = GAME_OVER
                    self.ship.points_when_died = self.score
                    for obstacle in self.obstacle_list:
                        obstacle.is_active = False

        # --- SIMULATION MODE (MULTIPLE SHIPS) ---
        else:

            for ship in self.population.ships_list:
                if ship.alive:
                    if 0 <= ship.position_x <= closest_obstacle_x1 or closest_obstacle_x2 <= ship.position_x <= 640:
                        if ship.center_y >= closest_obstacle_bottom_edge:

                            ship.alive = False
                            ship.points_when_died = self.score
                            self.count_dead += 1

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()

        if self.current_state == MENU:
            self.draw_menu()

        if self.current_state == GAME_RUNNING:
            self.draw_game()

        if self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()

    def ident_clos_obstacle(self):
        """Identifies closest obstacle. """

        if self.obstacle_list[self.closest_obstacle].position_y < 70:
            if self.closest_obstacle == 3:
                self.closest_obstacle = 0
            else:
                self.closest_obstacle += 1

    def update(self, delta_time):

        # --- SINGLE SHIP MODE ---
        if not self.simulation_mode:
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

        # --- POPULATION MODE (MULTIPLE SHIPS) ---
        else:
            if self.population.generation_id == NUMBER_OF_GENERATIONS:
                self.current_state = GAME_OVER

            if self.current_state == GAME_RUNNING:

                # --- EVOLUTION ---
                if self.count_dead >= POPULATION_SIZE:

                    # Deactivate obstacles
                    for obstacle in self.obstacle_list:
                        obstacle.is_active = False

                    # Reset score
                    self.score = 0

                    # Evolve
                    self.population.evolve()

                    # Reactivate obstacles
                    for obstacle in self.obstacle_list:
                        obstacle.is_active = True

                    self.count_dead = 0

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

                self.check_for_collision()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """

        if self.current_state == MENU:
            if key == arcade.key.A:
                self.current_state = GAME_RUNNING
                self.AI_mode = True
                self.simulation_mode = False
                self.setup()
            if key == arcade.key.B:
                self.current_state = GAME_RUNNING
                self.AI_mode = False
                self.simulation_mode = False
                self.setup()
            if key == arcade.key.C:
                self.current_state = GAME_RUNNING
                self.AI_mode = True
                self.simulation_mode = True
                self.setup()

        if self.current_state == GAME_RUNNING:
            if not self.simulation_mode:
                if self.ship.alive:
                    if not self.AI_mode:
                        if key == arcade.key.LEFT:
                            self.ship.change_x = -MOVEMENT_SPEED
                        elif key == arcade.key.RIGHT:
                            self.ship.change_x = MOVEMENT_SPEED

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
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
