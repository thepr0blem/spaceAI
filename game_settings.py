""" Game settings """

# Screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Game parameters
MOVEMENT_SPEED = 10
OBSTACLE_SPEED = 250
NO_OBSTACLES = 4
OBSTACLE_FREQ = int(SCREEN_HEIGHT/(NO_OBSTACLES - 1))

# Game states
MENU = 0
GAME_RUNNING = 1
GAME_OVER = 2
EVOLUTION = 3
SIMULATION_MENU = 4

# Population
POPULATION_SIZE = 100    # Must be > 5
MUTATION_SCALE = 0.3    # Previous best 0.2
MUTATION_PROB = 0.5     # Previous best 0.2
SELECTION_RATE = 0.3
BEST_GEN_A_PATH = r"./generation_logs/top_gen_a.npy"
BEST_GEN_B_PATH = r"./gerneration_logs/top_gen_b.npy"