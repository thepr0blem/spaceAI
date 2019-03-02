import arcade
from settings import *


class Drawer:
    """
    Helper class - collection of method used by MyGame class to draw different possible scenarios, like:
    - current game state
    - menu screens
    - game over screen
    - bottom bar with score/additional information
    """

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

        self.draw_bottom_bar(score=self.score,
                             simulation_mode=self.simulation_mode,
                             gen_id=self.population.generation_id,
                             living_ships=self.population.living_ships,
                             gap_x1=self.obstacle_list[self.closest_obstacle].gap_x1,
                             gap_x2=self.obstacle_list[self.closest_obstacle].gap_x2,
                             pos_y=self.obstacle_list[self.closest_obstacle].position_y)

    def draw_menu(self):
        """Draw MENU screen. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("Choose game mode: ", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 70,
                         arcade.color.WHITE, 28, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("A. Random Autopilot", 170, 280,
                         arcade.color.WHITE, 20, anchor_x="left", anchor_y="top")
        arcade.draw_text("B. Human Player", 170, 240,
                         arcade.color.WHITE, 20, anchor_x="left", anchor_y="top")
        arcade.draw_text("C. Simulation", 170, 200,
                         arcade.color.WHITE, 20, anchor_x="left", anchor_y="top")

    def draw_game_over(self, points):
        """Draw GAME OVER screen. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("Game Over", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 70,
                         arcade.color.WHITE, 50, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("1. SPACE to restart", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text("2. ENTER to return to MENU", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 40,
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text(f"Score: {points}",
                         int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) - 80,
                         arcade.color.WHITE, 16, align="center", anchor_x="center", anchor_y="center")

    def draw_evo_state(self):
        """Displays EVOLUTION screen when calculating new generation. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("Evolution", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                         arcade.color.WHITE, 54, align="center", anchor_x="center", anchor_y="center")

    def draw_sim_menu(self):
        """Displays SIMULATION menu on the screen. """

        arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
        arcade.draw_text("Simulation MENU:", 30, 310,
                         arcade.color.WHITE, 28, anchor_x="left", anchor_y="top")
        arcade.draw_text("1. SPACE to restart simulation", 30, 260,
                         arcade.color.WHITE, 18, anchor_x="left", anchor_y="top")
        arcade.draw_text("2. Click ESC to leave to MAIN menu", 30, 220,
                         arcade.color.WHITE, 18, anchor_x="left", anchor_y="top")

    def draw_bottom_bar(self, score, simulation_mode, gen_id, living_ships, gap_x1, gap_x2, pos_y):
        """Displays bottom info bar on the screen. """

        # Drawing bottom screen area with score and dist to closest obstacle
        arcade.draw_rectangle_filled(320, 15, 640, 30, arcade.color.BLACK)
        score_text = f"Score: {score}"
        arcade.draw_text(score_text, 10, 10, arcade.color.WHITE, 13)

        # Draws generation number and # of ships alive if in simulation mode
        if simulation_mode:

            gen_id = f"gen_id: {gen_id}"
            arcade.draw_text(gen_id, 90, 10, arcade.color.WHITE, 13)

            live_ships = f"ships_alive: {living_ships}"
            arcade.draw_text(live_ships, 180, 10, arcade.color.WHITE, 13)

            arcade.draw_text("R to enter simulation MENU", 305, 10, arcade.color.WHITE, 13)

        # Draws coordinates and distance to closest obstacle if in single-player mode
        else:
            # Display x1 and x2 coordinates of gap in closest obstacle
            near_obs_x1 = f"gap_x1 = {round(gap_x1)}"
            arcade.draw_text(near_obs_x1, 330, 10, arcade.color.WHITE, 13)

            near_obs_x1 = f"gap_x2 = {round(gap_x2)}"
            arcade.draw_text(near_obs_x1, 450, 10, arcade.color.WHITE, 13)

            # Distance to closest objects (delta y)
            near_obs_y = f"Closest obstacle: delta_y = " \
                f"{int(round(pos_y - 70, -1))}"
            arcade.draw_text(near_obs_y, 90, 10, arcade.color.WHITE, 13)
