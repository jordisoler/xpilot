"""
    Used constants.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

TARGET = (1000, 1000)
DATA_FILE = "last_game.csv" # File name to store game data
# HOST = "147.83.26.103"
HOST = "localhost"          # Server IP

PLAYER_NAME = "jordi"       # Player name

# Map size
MAP_WIDTH = 3000
MAP_HEIGHT = 3000

WALL_MARGIN = 500           # Margin to be kept with the walls

FIRE_GAIN = 3

SHIP_ACC = 1.7              # Ship acceleration (computed offline)
MAX_VEL = 25                # Maximum ship velocity allowed

ON = 1                      # Thrust on
OFF = 0                     # Thrust off

ORIENTATION_TH = 2.0        # Orientation threshold in degrees

CLF_THR = 0.3               # Classification Threshold. Minimum score of
                            #       an action to change the current action

DISTANCE_TO_ENEMY = 25

MAX_TURN_SPEED = "64"
TURN_SPEED = MAX_TURN_SPEED

# Set of selectable actions
import action
import fire
import moveAt
ACTIONS = [action.DoNothing, moveAt.GoCenter, moveAt.AvoidWall, \
        moveAt.SurroundClosestEnemy, fire.FireClosestEnemy]
