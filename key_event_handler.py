import arcade
from settings import *


class KeyEventHandler:
    """
    Helper class - collection of methoded used to track keyboard presses and handling respective actions
    """

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """

        if not self.simulation_mode:
            if self.ship.alive:
                if key == arcade.key.LEFT or key == arcade.key.RIGHT:
                    self.ship.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever the user presses a key. """

        # --- MAIN MENU BUTTONS --- #
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
                self.population.erase_history()

        # --- GAME RUNNING BUTTONS --- #
        if self.current_state == GAME_RUNNING:

            # - SIMULATION MODE (MULTIPLE SHIPS) -
            if self.simulation_mode:
                if key == arcade.key.R:
                    self.current_state = SIMULATION_MENU

            # - SINGLE SHIP MODE -
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
                self.population.break_simulation(self.score)
                self.current_state = MENU
            elif key == arcade.key.SPACE:
                self.current_state = GAME_RUNNING
                self.population.erase_history()
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
