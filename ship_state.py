"""
    This file hosts the class ShipState.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""
from moveAt import MoveAt


class ShipState(object):
    """
        Holds data from frame to frame and handles basic processes related
        with the ship state.
    """
    def __init__(self):
        self.action = None
        self.ai = None

    def sey_hi(self):
        """ Dummy function for debugging purposes """
        print("Hi! I'm the ship state.")

    def set_ai(self, ai):
        """ Set the xpilot handler """
        self.ai = ai

    def set_action(self, act):
        """ Sets the current action """
        self.action = act
        self.selectAction(act)

    def act(self):
        """ Act according to the current action """
        print("ShipState: Taking action.")
        self.action.act(self.ai)

    def current_action(self):
        """ Returns the ship current action """
        return self.action


    def selectAction(self, name):
        """ Selects an action given its name """
        if name == "move_at":
            self.action = MoveAt("hola")
        else:
            print("ShipState: The name %s does not corrspond to any valid action" % name)
