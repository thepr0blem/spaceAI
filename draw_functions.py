import arcade
from settings import *


def draw_menu():
    """Draw MENU screen. """

    arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
    arcade.draw_text("Choose game mode: ", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5) + 90,
                     arcade.color.WHITE, 28, align="center", anchor_x="center", anchor_y="center")
    arcade.draw_text("A. Random Autopilot", 170, 300,
                     arcade.color.WHITE, 20, anchor_x="left", anchor_y="top")
    arcade.draw_text("B. Human Player", 170, 260,
                     arcade.color.WHITE, 20, anchor_x="left", anchor_y="top")
    arcade.draw_text("C. Simulation", 170, 220,
                     arcade.color.WHITE, 20, anchor_x="left", anchor_y="top")
    arcade.draw_text("D. Top Pilot", 170, 180,
                     arcade.color.WHITE, 20, anchor_x="left", anchor_y="top")


def draw_game_over(points):
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


def draw_evo_state():
    """Displays EVOLUTION screen when calculating new generation. """

    arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
    arcade.draw_text("Evolution", int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5),
                     arcade.color.WHITE, 54, align="center", anchor_x="center", anchor_y="center")


def draw_sim_menu():
    """Displays SIMULATION menu on the screen. """

    arcade.draw_rectangle_filled(int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.5), 700, 250, arcade.color.BLACK)
    arcade.draw_text("Simulation MENU:", 30, 350,
                     arcade.color.WHITE, 28, anchor_x="left", anchor_y="top")
    arcade.draw_text("1. SPACE to restart simulation", 30, 300,
                     arcade.color.WHITE, 18, anchor_x="left", anchor_y="top")
    arcade.draw_text("2. S to save best genes from latest generation", 30, 260,
                     arcade.color.WHITE, 18, anchor_x="left", anchor_y="top")
    arcade.draw_text("3. Click ESC to leave to MAIN menu", 30, 220,
                     arcade.color.WHITE, 18, anchor_x="left", anchor_y="top")


def draw_bottom_bar(score, simulation_mode, gen_id, living_ships, gap_x1, gap_x2, pos_y):
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
