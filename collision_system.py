from settings import *


class CollisionSystem:

    def check_for_collision(self):
        """Checks for collision between ship / population of ships and closest obstacle. """

        # Calculating y position of closest obstacle bottom edge
        clo_obst_bot_edge = self.obstacle_list[self.closest_obstacle].position_y \
                                       - self.obstacle_list[self.closest_obstacle].thickness * 0.5

        # Calculating x1, x2 positions of gap in closest obstacle
        clo_obst_x1 = self.obstacle_list[self.closest_obstacle].gap_x1
        clo_obst_x2 = self.obstacle_list[self.closest_obstacle].gap_x2

        # --- COLLISONS IN SIMULATION MODE (MULTIPLE SHIPS) ---
        if self.simulation_mode:

            for ship in self.population.ships_list:
                if ship.alive:
                    if 0 <= ship.position_x <= clo_obst_x1 or clo_obst_x2 <= ship.position_x <= 640:
                        if ship.center_y >= clo_obst_bot_edge:
                            ship.alive = False
                            ship.pilot.pilot_score = self.score
                            ship.pilot.calc_fitness()

        # --- COLLISIONS IN SINGLE SHIP MODE ---
        else:
            if 0 <= self.ship.position_x <= clo_obst_x1 or clo_obst_x2 <= self.ship.position_x <= 640:
                if self.ship.center_y >= clo_obst_bot_edge:

                    self.ship.alive = False
                    self.current_state = GAME_OVER
                    self.ship.pilot.pilot_score = self.score
                    for obstacle in self.obstacle_list:
                        obstacle.is_active = False

    def ident_clos_obstacle(self):
        """Identifies closest obstacle. """

        # Take the next obstacle form the list if y position of the current closest obstacle is smaller
        # than y position of center of the ship
        if self.obstacle_list[self.closest_obstacle].position_y < 70:
            if self.closest_obstacle == 3:
                self.closest_obstacle = 0
            else:
                self.closest_obstacle += 1

    def pass_obstacles(self):
        """Updating closest obstacle. """
        # Passing obstacles
        prev_obst = self.closest_obstacle  # passed obstacle
        self.ident_clos_obstacle()  # identifying new obstacle
        curr_obst = self.closest_obstacle  # assigning new obstacle
        if not prev_obst == curr_obst:  # if obstacle changed, add +1 point
            self.score += 1
            for obstacle in self.obstacle_list:
                obstacle.level_up(self.score)
