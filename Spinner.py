#Xpilot-AI Team 2012
#Run: python3 Spinner.py
import libpyAI as ai
import math
import os

from constants import *
from ship_state import ShipState
from moveAt import MoveAt


def angle_diff(alpha, beta):
    """ Computes the absolute minimum distance between two angles """

    ang_abs = math.fabs(alpha-beta)
    return ang_abs if ang_abs < 180. else angle_diff(ang_abs - 360, 0)


def move(position):
    """ Move to a certain point in the map """

    t_ang = math.atan2(position[1] - ai.selfY(), position[0] - ai.selfX())
    t_ang_deg = t_ang * 180. / 3.1415
    # print("Angles. Desired: %f, current: %f, diff: %f" % \
            # (t_ang_deg, ai.selfHeadingDeg(), angle_diff(t_ang_deg, ai.selfHeadingDeg())))
    print("Position: (%u, %u). Velocity: (%u, %u)" % \
            (ai.selfX(), ai.selfY(), ai.selfVelX(), ai.selfVelY()))
    if angle_diff(t_ang_deg, ai.selfHeadingDeg()) > 3.0:
        ai.turnToDeg(int(t_ang_deg))
    # else:
        # ai.thrust(1)


def register():
    """ Register sensor data in a CSV file """

    data = {}
    data["X"] = ai.selfX()
    data["Y"] = ai.selfY()
    data["VelX"] = ai.selfVelX()
    data["VelY"] = ai.selfVelY()

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


def ai_loop():
    """ Main loop. Automatically run at each frame. """

    first_time = register()
    if first_time:
        initialise()
        ship.set_action("move_at")
        ship.set_ai(ai)

    ship.act()

    #ai.shield()
    #ai.fireShot()
    #ai.presskey(KEY_FIRE_LASER)
    #print("Position: (%u, %u)" % (ai.selfX(), ai.selfY()))
    #print("Radar: (%u, %u)" % (ai.selfRadarX(), ai.selfRadarY()))
    #print(ai.selfHeadingDeg())
    # diff = math.sqrt((ai.selfX()-TARGET[0])**2 +(ai.selfY()-TARGET[1])**2)
    # print("diff: %f" % diff)
    # if diff > 50.0:
        # move(TARGET)
        # ai.thrust(1)
    # else:
        # ai.thrust(0)
        # print("Done!")
    #ai.turn(1.23)


open(DATA_FILE, "w").close()
ship = ShipState()

ai.start(ai_loop, ["-name", PLAYER_NAME, "-join", HOST])
