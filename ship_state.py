"""
    This file hosts the class ShipState.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""
from constants import ACTIONS


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

        if act is None:
            return

        action_name = act if type(act) == str else ACTIONS[act].__name__
        print("Action name is :", action_name)

        # Check that new action is a valid action different than the current one
        if action_name != self.current_action():
            self.target = target
            self.select_action(action_name)

    def act(self):
        """ Act according to the current action """
        try:
            self.action.act()
        except AttributeError:
            print("Action not yet initialised!")

    def current_action(self):
        """ Returns the ship current action """
        return None if self.action is None else type(self.action)


    def select_action(self, name):
        """ Selects an action given its name """
        # print("handling "+name)
        # if name == "move_at":
            # self.action = MoveAt(self.target)
        # elif name == "go_center":
            # self.action = GoCenter()
        # elif name == "avoid_wall":
            # self.action = AvoidWall()
        # elif name == "fire":
            # self.action = Fire(self.target)
        # elif name == "do_nothing":
            # self.action = DoNothing()
        # else:
            # print("ShipState: The name %s does not correspond to any valid action" % name)
        action_types = [atype for atype in ACTIONS if atype.__name__ == name]

        if len(action_types) > 1:
            print("There is more than one action with name '%"+name+"'.")
        elif len(action_types) == 0:
            print("Name '"+name+"' does not name a valid action.")
            print("Valid names are: ", ", ".join(act.__name__ for act in ACTIONS))
        else:
            print("Setting action: "+name)
            if self.action is not None:
                self.action.preempt()
            self.action = action_types[0]()


    def select_action_num(self, num):
        self.action = ACTIONS[num]()
        print("Setting action: "+type(self.action))



