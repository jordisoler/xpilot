""" File containing tools for the Xpilot autopilot """
import math
import libpyAI as ai

def angle_diff(alpha, beta):
    """ Computes the absolute minimum distance between two angles """

    ang_abs = math.fabs(alpha-beta)
    return ang_abs if ang_abs < 180. else angle_diff(ang_abs - 360, 0)


def distance_to(goal, origin=None):
    if origin is None:
        origin = (ai.selfX(), ai.selfY())

    return math.hypot(goal[0]-origin[0], goal[1]-origin[1])

