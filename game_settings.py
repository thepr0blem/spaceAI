""" Game settings """

# Screen size
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Game parameters
MOVEMENT_SPEED = 10
OBSTACLE_SPEED = 150
NO_OBSTACLES = 4
OBSTACLE_FREQ = int(SCREEN_HEIGHT/(NO_OBSTACLES - 1))

# Game states
MENU = 0
GAME_RUNNING = 1
GAME_OVER = 2

# Memory of population
# TODO - develop structure for
#  keeping scores and genomes between generations
