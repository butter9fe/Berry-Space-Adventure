# Just stores all the global constant variables lol
# Canvas
CANVAS_MULTIPLIER = 10 # How many times the canvas is bigger than the window
CANVAS_X_STARTOFFSET = 0.5 # Beginning position of canvas in X direction
CANVAS_Y_STARTOFFSET = 0.1 # Beginning position of canvas in Y direction

# Physics
GRAVITY = 0.05
PLAYER_SHOOT_STRENGTH = 0.015
WALL_VELOCITY_DIMINISH_MULTIPLIER = 0.6
ENERGY_DEPLETION = 0.1
ENERGY_TO_JUMP = 30
ENERGY_GAIN_FROM_STAR = 60

# Game
MAX_STARS = 10 # Maximum stars that are on-screen at a time
MIN_GAP_BTW_OBJS = 10 # MInimum gap between game objects
MAX_RANDOM_ATTEMPTS = 10 # Maximum number of attempts to generate a random position
OFFSCREEN_SPAWN_MULTIPLIER = 0.25 # How far away from the canvas edge can things spawn, in relation to the window size