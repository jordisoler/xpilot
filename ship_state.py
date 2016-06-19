"""
    This file hosts the class ShipState.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""
import libpyAI as ai
from constants import ACTIONS


class ShipState(object):
    """
        Holds data from frame to frame and handles basic processes related
        with the ship state.
    """
    def __init__(self):
        self.action = None
        self.target = None
        self.warned = False
        self.was_dead = ai.selfAlive()
        self.was_dead_before = ai.selfAlive()

    def set_action(self, act, target=None):
        """ Sets the current action """

        if act is None:
            return

        action_name = act if type(act) == str else ACTIONS[act].__name__

        # Check that new action is a valid action different than the current one
        if action_name != self.current_action():
            self.target = target
            self.select_action(action_name)

    def act(self):
        """ Act according to the current action """
        if self.was_dead:
            for _ in range(2): ai.shield()
            self.was_dead = False
        elif self.was_dead_before:
            if not ai.selfShield(): ai.shield()
            self.was_dead_before = False

        try:
            self.action.act()
        except AttributeError:
            if not self.warned:
                print("Action not yet initialised!")
                self.warned = True

    def current_action(self):
        """ Returns the ship current action """
        return "None" if self.action is None else self.action.__class__.__name__


    def select_action(self, name):
        """ Selects an action given its name """
        action_types = [atype for atype in ACTIONS if atype.__name__ == name]

        if len(action_types) > 1:
            print("There is more than one action with name '"+name+"'.")
        elif len(action_types) == 0:
            print("Name '"+name+"' does not name a valid action.")
            print("Valid names are: ", ", ".join(act.__name__ for act in ACTIONS))
        else:
            print("Changing action: "+self.current_action()+" -> "+name)
            if self.action is not None:
                self.action.preempt()
            self.action = action_types[0]()


    def you_are_dead(self):
        """ Procedure to be run when the ship is dead. """
        if not self.was_dead:
            self.set_action("DoNothing")
            self.was_dead = True
            self.was_dead_before = True


