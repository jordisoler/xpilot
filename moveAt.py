"""
    This file hosts the class MoveAt.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import math
import sys
import traceback
import libpyAI as ai
import numpy as np
from action import Action
from constants import *
from xpilot_tools import angle_diff
from xpilot_tools import distance_to
from xpilot_tools import angle_to
from xpilot_tools import cart2pol

class MoveAt(Action):
    """
        Ship action that consists in moving the ship to a certain position.
        Due to the nature of the task the implamentation is rule-based.
    """
    def __init__(self, position=None):
        print("MoveAt: Initialising move at")
        if position is None:
            print("MoveAt: Target not specified!!")
            ai.quitAI()
            sys.exit(0)
        else:
            self.position = position
        self.state = "orienting"
        self.k_pos = 0.04
        self.k_vel = 0.02
        self.t_th = 0.02


    def control(self):
        """ Control the ship position. """
        try:
            pos = np.array([ai.selfX(), ai.selfY()])
            vel = np.array([ai.selfVelX(), ai.selfVelY()])
            orientation = ai.selfHeadingDeg() * 3.1415 / 180.

            #print("")
            #print("-"*80)
            #print("Pos: %s. Target: %s" % (pos, self.position))
            #print("Current angle: %f, ang_des: %f. speed_des: %f" % (orientation*180/3.14, ang_des*190/3.14, speed_des))

            vel_des = (self.position - pos) * self.k_pos
            acc_des = (vel_des - vel) * self.k_vel
            acc_mod, acc_ang = cart2pol(acc_des)

            #print("vel_des: %s, vel: %s. Acceleration: %s. Acc ang: %f" % (vel_des, vel, acc_des, acc_ang*180/3.1415))

            # ang_vels = angle_diff(vel, vel_des)
            # ai.turnToDeg(int(math.atan2(acc_des[1], acc_des[0])))

            print("Turning to %u. Current: %u" % (int(acc_ang * 180 / 3.1415), ai.selfHeadingDeg()))
            ai.turnToDeg(int(acc_ang * 180 / 3.1415))
            thrust_level = np.cos(angle_diff(orientation, acc_ang)) * acc_mod
            ai.thrust(thrust_level > self.t_th)

            #print("Cos: ", np.cos(angle_diff(orientation, acc_ang)))

            #print("""Velocity: %s, vel_des: %s, acc_des = %s, (%f, %u), thrust_level = %f"""\
            #        % (vel, vel_des, acc_des, acc_mod, int(acc_ang* 180 / 3.1415), thrust_level))
        except:
            print("Unexpected error, %s: %s" % sys.exc_info()[:2])
            print(traceback.print_tb(sys.exc_info()[-1]))


    def act(self):
        self.control()

    def preempt(self):
        ai.thrust(0)

    def is_done(self):
        return self.state == "done"


class GoCenter(MoveAt):
    """ Go to the center of the map """
    def __init__(self):
        middle = (MAP_WIDTH/2, MAP_HEIGHT/2)
        super().__init__(position=middle)

