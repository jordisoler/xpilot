"""
    This file hosts the class Fire.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import sys
import numpy as np
import libpyAI as ai
from action import Action
from xpilot_tools import angle_to
from constants import FIRE_GAIN

class Fire(Action):
    """
        Ship action that consists in shoting in a certain direction.
    """
    def __init__(self, target=None):
        self.name = "fire"
        if target is None:
            print("Fire: Target not specified!!")
            ai.quitAI()
            sys.exit(1)
        else:
            self.target = target
        if ai.selfShield():
            ai.shield()


    def change_target(self, newtarget):
        """ Change current target """
        self.target = newtarget


    def open_fire(self):
        """ Fires the selected target """
        angle = angle_to(self.target)
        ai.turnToDeg(int(angle))
        ai.fireShot()


    def act(self):
        self.open_fire()


    def preempt(self):
        if not ai.selfShield():
            ai.shield()


    def is_done(self):
        return False


class FireEnemy(Fire):
    """
        Opens fire to an enemy.
    """
    def __init__(self, idE=None, gain=FIRE_GAIN):
        if idE is None:
            print("FireEnemy: No enemy selected! Exiting now.")
            ai.quitAI()
            sys.exit(1)
        self.idE = idE
        self.K = gain


    def act(self):
        angle = ai.enemyHeadingDeg(self.idE)
        pos = np.array([ai.screenEnemyXId(self.idE), ai.screenEnemyYId(self.idE)])
        vel = ai.enemySpeedId(self.idE) * np.array([np.cos(angle), np.sin(angle)])
        self.target = pos - vel * self.K
        self.open_fire()


class FireClosestEnemy(FireEnemy):
    """ Opens fire to the closest enemy. """
    def __init__(self, gain=FIRE_GAIN):
        super(FireClosestEnemy, self).__init__(ai.closestShipId(), gain)


