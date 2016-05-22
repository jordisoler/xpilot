"""
    This file hosts the class Fire.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import sys
import libpyAI as ai
from action import Action
from xpilot_tools import angle_to

class Fire(Action):
    """
        Ship action that consists in shoting in a certain direction.
    """
    def __init__(self, target=None):
        if target is None:
            print("Fire: Target not specified!!")
            ai.quitAI()
            sys.exit(0)
        else:
            self.target = target
        if ai.selfShield():
            ai.shield()


    def change_target(self, newtarget):
        """ Change current target """
        self.target = newtarget


    def act(self):
        angle = angle_to(self.target)
        ai.turnToDeg(int(angle))
        ai.fireShot()


    def preempt(self):
        if not ai.selfShield():
            ai.shield()


    def is_done(self):
        return False

