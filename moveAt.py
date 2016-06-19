"""
    This file hosts the class MoveAt and its derived classes.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import sys
import traceback
from random import uniform
import libpyAI as ai
import numpy as np
from action import Action
from constants import WALL_MARGIN, MAP_WIDTH, MAP_HEIGHT, DISTANCE_TO_ENEMY
from xpilot_tools import angle_diff
from xpilot_tools import cart2pol

class MoveAt(Action):
    """
        Ship action that consists in moving the ship to a certain position.
    """
    def __init__(self, position=None):
        print("MoveAt: Initialising move at")
        if position is None:
            print("MoveAt: Target not specified!!")
            ai.quitAI()
            sys.exit(0)
        else:
            self.position = position
        self.setGains()
        self.done = False


    def setGains(self):
        self.k_pos = 0.04
        self.k_vel = 0.015
        self.t_th = 0.03


    def control(self, target=None):
        """ Control the ship position. """
        try:
            if target is None:
                target = self.position

            pos = np.array([ai.selfX(), ai.selfY()])
            vel = np.array([ai.selfVelX(), ai.selfVelY()])
            orientation = ai.selfHeadingDeg()

            vel_des = (target - pos) * self.k_pos
            acc_des = (vel_des - vel) * self.k_vel
            acc_mod, acc_ang = cart2pol(acc_des)

            #print("vel_des: %s, vel: %s. Acceleration: %s. Acc ang: %f" % (vel_des, vel, acc_des, acc_ang*180/3.1415))

            # ang_vels = angle_diff(vel, vel_des)
            # ai.turnToDeg(int(math.atan2(acc_des[1], acc_des[0])))
            # print("")
            # print("-"*80)

            ang_des = int(acc_ang if acc_ang > 0 else acc_ang + 360)
            # print("Turning to %u. Current: %u" % (ang_des, ai.selfHeadingDeg()))
            ai.turnToDeg(ang_des)
            thrust_level = np.cos(angle_diff(orientation, acc_ang)) * acc_mod
            ai.thrust(thrust_level > self.t_th)

            # print("Pos: %s. Target: %s" % (pos, self.position))
            # print("Current angle: %f, ang_des: %f." % (orientation, ang_des))

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
        return self.done


class GoCenter(MoveAt):
    """ Go to the center of the map """
    def __init__(self):
        middle = (MAP_WIDTH/2, MAP_HEIGHT/2)
        super().__init__(position=middle)


class AvoidWall(MoveAt):
    """
        Ship action that consists in moving the ship away from the walls.
    """
    def __init__(self):
        pos = [MAP_HEIGHT, MAP_WIDTH]
        super().__init__(position=pos)


    def act(self):
        pos = [ai.selfX(), ai.selfY()]
        goal = []
        for coord, maximum in zip(pos, self.position):
            goal.append(max(min(coord, maximum - WALL_MARGIN), WALL_MARGIN))

        self.done = pos == goal
        if pos != goal:
            self.control(goal)


class SurroundEnemy(MoveAt):
    """
        Moves the ship to a random position at a certain distance of an enemy
    """
    def __init__(self, idE):
        self.idE = idE
        angle = uniform(0, np.pi)
        offset = DISTANCE_TO_ENEMY * np.array([np.cos(angle), np.sin(angle)])
        self.pos_offset = [np.round(coord) for coord in offset]
        enemy_pos = np.array([ai.screenEnemyXId(idE), ai.screenEnemyYId(idE)])
        pos = enemy_pos + self.pos_offset
        super().__init__(position=[np.round(coord) for coord in pos])


    def act(self):
        enemy_pos = np.array([ai.screenEnemyXId(self.idE), ai.screenEnemyYId(self.idE)])
        self.position = enemy_pos + self.pos_offset 
        self.control()


class SurroundClosestEnemy(SurroundEnemy):
    """
        SurroundEnemy applied to the closest one
    """
    def __init__(self):
        idE = ai.closestShipId()
        super().__init__(idE)
