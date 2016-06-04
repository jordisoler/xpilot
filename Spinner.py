#Xpilot-AI Team 2012
#Run: python3 Spinner.py
import libpyAI as ai
import traceback
import sys
import os

from constants import *
from ship_state import ShipState
from moveAt import MoveAt, GoCenter
from actionSelector import ActionSelector


def register():
    """ Register sensor data in a CSV file """

    data = {}
    data["X"] = ai.selfX()
    data["Y"] = ai.selfY()
    data["VelX"] = ai.selfVelX()
    data["VelY"] = ai.selfVelY()
    data["Orientation"] = ai.selfHeadingDeg()

    # Check if it's the first iteration by checking if the data file is empty
    first_time = os.stat(DATA_FILE).st_size == 0

    with open(DATA_FILE, "a") as f:
        if first_time:
            f.write(";".join(data) + "\n")
        f.write(";".join(str(value) for value in data.values()) + "\n")

    return first_time


def initialise():
    """ Initial procedure """
    print("New Game!")
    ship.set_action("avoid_wall", target=TARGET)


def ai_loop():
    """ Main loop. Automatically run at each frame. """

    try:
        first_time = register()
        if first_time:
            initialise()

        action = actSelector.decide()
        if action is not None and action != ship.current_action():
            ship.set_action(action)
        ship.act()
    except:
        print("Unexpected error, %s: %s" % sys.exc_info()[:2])
        print(traceback.print_tb(sys.exc_info()[-1]))


open(DATA_FILE, "w").close()
ship = ShipState()
actSelector = ActionSelector()

ai.start(ai_loop, ["-name", PLAYER_NAME, "-join", HOST, "-turnSpeed", MAX_TURN_SPEED])
