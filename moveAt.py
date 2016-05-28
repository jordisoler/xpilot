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
        self.k_pos = 0.025
        self.k_vel = 0.005
        self.t_th = 2.5


    def d_critic_reached(self, orient=True):
        """ Check if critical distance is reached

          Current      fully            ship
           Ship        turned           stopped
            |>           o                x       target
            |<--d_turn-->|<----d_brake--->|         |
            |<---------d_critic---------->|         |
            |<-------------g_goal------------------>|
        """
        d_goal = distance_to(self.position)         # Distance to goal
        d_turn = ai.selfSpeed() * TURNING_FRAMES    # Distance needed to turn
        d_brake = 1.0 * ai.selfSpeed()**2 / SHIP_ACC    # Distance to brake at full power

        d_critic = d_turn + d_brake if orient else d_brake
        print("Critic distance: %f, goal distance: %f" % (d_critic, d_goal))
        return d_goal <= d_critic


    def control(self):
        """ Control the ship position. """
        try:
            pos = np.array([ai.selfX(), ai.selfY()])
            vel = np.array([ai.selfVelX(), ai.selfVelY()])
            orientation = ai.selfHeadingDeg() * 3.1415 / 180.

            ang_des = angle_to(self.position) * 3.1415 / 180.
            speed_des = distance_to(self.position) * self.k_pos

            print("")
            print("-"*80)
            print("Pos: %s. Target: %s" % (pos, self.position))
            print("Current angle: %f, ang_des: %f. speed_des: %f" % (orientation*180/3.14, ang_des*190/3.14, speed_des))

            vel_des = self.position - pos
            acc_des = (vel_des - vel) * self.k_vel
            acc_mod, acc_ang = cart2pol(acc_des)

            print("vel_des: %s, vel: %s. Acceleration: %s. Acc ang: %f" % (vel_des, vel, acc_des, acc_ang*180/3.1415))

            # ang_vels = angle_diff(vel, vel_des)
            # ai.turnToDeg(int(math.atan2(acc_des[1], acc_des[0])))

            ai.turnToDeg(int(acc_ang * 180 / 3.1415))
            thrust_level = np.cos(angle_diff(orientation, acc_ang)) * acc_mod
            ai.thrust(thrust_level > self.t_th)

            print("Cos: ", np.cos(angle_diff(orientation, acc_ang)))

            print("""Velocity: %s, vel_des: %s, acc_des = %s, (%f, %u), thrust_level = %f"""\
                    % (vel, vel_des, acc_des, acc_mod, int(acc_ang* 180 / 3.1415), thrust_level))
        except:
            print("Unexpected error, %s: %s" % sys.exc_info()[:2])
            print(traceback.print_tb(sys.exc_info()[-1]))


    def orienting(self):
        """ Orienting the ship towards the goal"""
        # print("Orienting towards: ", self.position)

        # Computing angle to the goal
        t_ang = math.atan2(self.position[1] - ai.selfY(),\
                self.position[0] - ai.selfX())
        t_ang_deg = t_ang * 180. / 3.1415
        if t_ang_deg < 0:
            t_ang_deg += 360
        # print("Angles. Desired: %u, current: %f, diff: %f" % \
                # (int(t_ang_deg), ai.selfHeadingDeg(), angle_diff(t_ang_deg, ai.selfHeadingDeg())))

        # Check for proper orientation
        if angle_diff(t_ang_deg, ai.selfHeadingDeg()) > ORIENTATION_TH:
            # Turn to the proper direction
            ai.turnToDeg(int(t_ang_deg))
        else:
            print("Orientation done")
            # Transition to the next state
            self.state = "launching"
            ai.thrust(ON)


    def launching(self):
        """
            The ship is accelerating.
            It is assumed that thrust is ON and correct direction
        """

        maximum_vel_reached = ai.selfSpeed() > MAX_VEL

        # Handling state transitions
        if maximum_vel_reached or self.d_critic_reached():
            ai.thrust(OFF)
            self.state = "hovering"
            print("Launching done")

    def hovering(self):
        """ State between acceleration and deceleration """
        t_ang = math.atan2(ai.selfVelY(), ai.selfVelX())
        t_ang_deg = t_ang * 180. / 3.1415

        ang_brake = t_ang_deg + 180

        if angle_diff(ang_brake, ai.selfHeadingDeg()) > ORIENTATION_TH:
            # Turn to the proper direction
            ai.turnToDeg(int(ang_brake))
        elif self.d_critic_reached(orient=False):
            # Transition to the next state
            self.state = "braking"
            ai.thrust(ON)
            print("Hovering done")


    def braking(self):
        """ Deceleration state """
        if ai.selfSpeed() < 2.0:
            ai.thrust(OFF)
            self.done = True
            print("Braking done")
            print("Position: (%u, %u). Target: (%u, %u)" % (ai.selfX(),\
                    ai.selfY(), self.position[0], self.position[1]))
            self.state = "done"


    def act(self):
        self.control()


        # if self.state == "orienting":
            # self.orienting()
        # elif self.state == "launching":
            # self.launching()
        # elif self.state == "hovering":
            # self.hovering()
        # elif self.state == "braking":
            # self.braking()
        # elif self.state == "done":
            # pass
        # else:
            # print("Bad MoveAt state: ", self.state)

    def preempt(self):
        ai.thrust(0)

    def is_done(self):
        return self.state == "done"


class GoCenter(MoveAt):
    """ Go to the center of the map """
    def __init__(self):
        print("hola")
        middle = (MAP_WIDTH/2, MAP_HEIGHT/2)
        print("dew")
        super().__init__(position=middle)
        print("dewww")

