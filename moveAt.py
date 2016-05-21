"""
    This file hosts the class MoveAt.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import libpyAI as ai
from action import Action

class MoveAt(Action):
    """ Ship action that consists in moving the ship to a certain position """
    def __init__(self, position):
        self.position = position

    def init(self):
        pass

    def act(self, ai):
        ai.thrust(1)

    def preempt(self, ai):
        ai.thrust(0)

    def is_done(self):
        return False

