"""
    This file hosts the class ShipState.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""
from moveAt import MoveAt, GoCenter, AvoidWall
from fire import Fire


class ShipState(object):
    """
        Holds data from frame to frame and handles basic processes related
        with the ship state.
    """
    def __init__(self):
        self.action = None
        self.target = None

    def set_action(self, act, target=None):
        """ Sets the current action """
        if self.action is not None:
            self.action.preempt()
        self.target = target
        self.selectAction(act)

    def act(self):
        """ Act according to the current action """
        self.action.act()

    def current_action(self):
        """ Returns the ship current action """
        return self.action.name


    def selectAction(self, name):
        """ Selects an action given its name """
        print("handling "+name)
        if name == "move_at":
            self.action = MoveAt(self.target)
        elif name == "go_center":
            self.action = GoCenter()
        elif name == "avoid_wall":
            self.action = AvoidWall()
        elif name == "fire":
            self.action = Fire(self.target)
        else:
            print("ShipState: The name %s does not correspond to any valid action" % name)

