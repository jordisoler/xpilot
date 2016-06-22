#Xpilot-AI Team 2012
#Run: python3 Spinner.py
import libpyAI as ai
import traceback
import numpy as np
import sys
import os

from constants import *
from ship_state import ShipState
from moveAt import MoveAt, GoCenter
from actionSelector import ActionSelector


def register():
    """ Register sensor data in a CSV file """

    cl_enemy = ai.closestShipId()
    data = {}
    data["Action"] = ship.current_action()
    data["X"] = ai.selfX()
    data["Y"] = ai.selfY()
    data["VelX"] = ai.selfVelX()
    data["VelY"] = ai.selfVelY()
    data["RadarX"] = ai.selfRadarX()
    data["RadarY"] = ai.selfRadarY()
    data["Orientation"] = ai.selfHeadingDeg()
    data["ClosestRadarX"] = ai.closestRadarX()
    data["ClosestRadarY"] = ai.closestRadarY()
    data["ClosestItemX"] = ai.closestItemX()
    data["ClosestItemY"] = ai.closestItemY()
    data["EnemySpeed"] = ai.enemySpeedId(cl_enemy)
    data["EnemyX"] = ai.screenEnemyXId(cl_enemy)
    data["EnemyY"] = ai.screenEnemyYId(cl_enemy)
    data["EnemyHeading"] = ai.enemyHeadingDegId(cl_enemy)
    data["EnemyShield"] = ai.enemyShieldId(cl_enemy)
    data["EnemyDistance"] = ai.enemyDistanceId(cl_enemy)
    data["ShotAlert"] = ai.shotAlert(0)
    data["ShotDist"] = ai.shotDist(0)
    data["ShotVel"] = ai.shotVel(0)
    data["ShotVelDir"] = ai.shotVelDir(0)

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
    ship.set_action("do_nothing")
    for _ in range(3): ai.shield() # Avoid initial shield locking


def ai_loop():
    """ Main loop. Automatically run at each frame. """

    try:
        first_time = register()
        if first_time:
            initialise()

        if ai.selfAlive():
            action = actSelector.decide()
            if action is not None:
                ship.set_action(action)

            ship.act()
        else:
            ship.you_are_dead()
    except:
        print("Unexpected error, %s: %s" % sys.exc_info()[:2])
        print(traceback.print_tb(sys.exc_info()[-1]))


open(DATA_FILE, "w").close()
ship = ShipState()
actSelector = ActionSelector()

ai.start(ai_loop, ["-name", PLAYER_NAME, "-join", HOST, "-turnSpeed", TURN_SPEED])
