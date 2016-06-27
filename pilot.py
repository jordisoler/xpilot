#Xpilot-AI Team 2012
#Run: python3 Spinner.py
import libpyAI as ai
import traceback
import numpy as np
import warnings
import sys
import os

from constants import *
from ship_state import ShipState
from moveAt import MoveAt, GoCenter
from actionSelector import ActionSelector
from classifier import get_readings

warnings.filterwarnings("ignore")


def register():
    """ Register sensor data in a CSV file """

    data = get_readings()
    data["Action"] = ship.current_action()

    # Check if it's the first iteration by checking if the data file is empty
    first_time = os.stat(DATA_FILE).st_size == 0

    if ai.selfAlive():
        with open(DATA_FILE, "a") as f:
            if first_time:
                f.write(";".join(data) + "\n")
            f.write(";".join(str(value) for value in data.values()) + "\n")

    return first_time


def initialise():
    """ Initial procedure """
    print("New Game!")
    ship.set_action("do_nothing")
    for _ in range(3): ai.shield() # Avoid initial shield locking


def ai_loop():
    """ Main loop. Automatically run at each frame. """

    try:
        first_time = register()
        if first_time:
            initialise()

        if ai.selfAlive():
            act = actSelector.decide()
            if action is not None:
                ship.set_action(act)

            ship.act()
        else:
            ship.you_are_dead()
    except:
        print("Unexpected error, %s: %s" % sys.exc_info()[:2])
        print(traceback.print_tb(sys.exc_info()[-1]))


open(DATA_FILE, "w").close()
ship = ShipState()
actSelector = ActionSelector(user=False)

ai.start(ai_loop, ["-name", PLAYER_NAME, "-join", HOST, "-turnSpeed", TURN_SPEED])
