"""
    This file contains utilities to choose the correct action to be taken.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import sys
import select

class ActionSelector(object):
    """ Selects the proper action to be taken. """
    def __init__(self, user=True):
        self.user = user
        # self.actions = {
                # "1" : "go_center",
                # "2" : "avoid_wall",
                # "3" : "fire"
                # }

    def action_pressed(self):
        """
            Returns last action specified by user in user mode.
            The user should specify the action by pressing
            the action number followed by [ENTER]

        """
        i, _, _ = select.select([sys.stdin], [], [], 0.0001)
        key = None
        for s in i:
            if s == sys.stdin:
                key = sys.stdin.readline()[-2]
        try:
            action = int(key)#self.actions[key]
        except:
            action = None
        return action


    def decide(self):
        """ Decide which action to take. """
        if self.user:
            return self.action_pressed()
        else:
            raise NotImplementedError("ActionSelector: Only user mode suported")

