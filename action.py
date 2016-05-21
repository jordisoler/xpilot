"""
    This file implements the action interface used for all actions.
    Its basically used for making sure that all actions can be called
    in the same way.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

class Action(object):
    """ Action object representiong a possible action of the ship. """

    def act(self):
        """ Main action """
        raise NotImplementedError("Method 'act' not implemented")

    def preempt(self):
        """ Procedure to be run when the action is preempted """
        raise NotImplementedError("Method 'preempt' not implemented")

    def is_done(self):
        """ True if the action has been completed """
        raise NotImplementedError("Method 'is_done' not implemented")
