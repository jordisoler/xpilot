"""
    This file hosts the class ShipState.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""
import action

class ShipState(object):
    """
        Holds data from frame to frame and handles basic processes related
        with the ship state.
    """
    def __init__(self):
        self.action = None

    def sey_hi(self):
        """ Dummy function for debugging purposes """
        print("Hi! I'm the ship state.")

    def set_action(self, act):
        """ Sets the current action """
        self.action = act

    def current_action(self):
        """ Returns the ship current action """
        return self.action
