""" SETTINGS """

# --- Screen size ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# --- Game parameters ---
MOVEMENT_SPEED = 12     # Ship movement speed
OBSTACLE_SPEED = 300
NO_OBSTACLES = 4
OBSTACLE_FREQ = int(SCREEN_HEIGHT/(NO_OBSTACLES - 1))   # Distance between obstacles

# --- Game states ---
MENU = 0
GAME_RUNNING = 1
GAME_OVER = 2
EVOLUTION = 3
SIMULATION_MENU = 4

# --- Evolution parameters ---
POPULATION_SIZE = 200    # Must be > 5
MUTATION_PROB = 0.1   # Previous best 0.2
SELECTION_RATE = 0.1
STAY_FRAC = 0.4

# --- Neural network parameters ---
NEURONS = 8
