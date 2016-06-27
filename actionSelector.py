"""
    This file contains utilities to choose the correct action to be taken.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import sys
import select
from constants import CLF_THR
from classifier import classifier

def action_pressed():
    """
        Returns last action specified by user in user mode.
        The user should specify the action by pressing
        the action number followed by [ENTER]

    """
    i, _, _ = select.select([sys.stdin], [], [], 0.0001)
    key = None
    try:
        for s in i:
            if s == sys.stdin:
                key = sys.stdin.readline()[-2]
        action = int(key)
    except IndexError:
        print("Bad key pressed")
        action = None
    except:
        action = None
    return action


class ActionSelector(object):
    """ Selects the proper action to be taken. """
    def __init__(self, user=True):
        self.user = user
        if not user:
            self.clf = classifier()
            self.clf.train()


    def decide(self):
        """ Decide which action to take. """
        if self.user:
            # User mode. Chooses action according to key (0, 1, 2, 3 or 4) pressed
            return action_pressed()
        else:
            # Bot mode. Chooses action by classifying current state
            act, score = self.clf.classify_state()
            print("Action: %s, score: %f" % (act, score))
            return act if score > CLF_THR else None

