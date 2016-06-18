"""
    This file implements an iterable action set to handle actions.

    This is part of the XPilot bot for the final project in
    Scientific Python for Engineers.
"""

import action
import fire
import moveAt

ACTIONS = [action.DoNothing, moveAt.GoCenter, \
        moveAt.AvoidWall, fire.FireEnemy, fire.FireClosestEnemy]
