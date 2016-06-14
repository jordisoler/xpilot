""" File containing tools for the Xpilot autopilot """
import math
import numpy as np
import libpyAI as ai
from constants import ON, OFF, TURN_SPEED

def angle_diff(alpha, beta, vectors=True, signed=False):
    """ Computes the absolute minimum distance between two angles """

    def getAngle(in_):
        try:
            return math.atan2(in_[1], in_[0])
        except:
            return in_

    if vectors:
        alpha, beta = map(getAngle, [alpha, beta])

    ang_abs = math.fabs(alpha-beta) if not signed else alpha-beta
    return ang_abs if ang_abs < 180. else angle_diff(ang_abs - 360, 0, vectors=False, signed=signed)


def cart2pol(cart):
    """ Get polar coordinates of a vector in cartesian coordinates """
    x, y = cart
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x) * 180. / 3.1415
    return (rho, phi)


def distance_to(goal, origin=None):
    """ Distance between two points in the game plane """
    if origin is None:
        origin = (ai.selfX(), ai.selfY())

    return math.hypot(goal[0]-origin[0], goal[1]-origin[1])


def angle_to(goal, origin=None):
    """ Angle between two points in the game plane """
    if origin is None:
        origin = (ai.selfX(), ai.selfY())

    t_ang = math.atan2(goal[1] - origin[1],\
            goal[0] - origin[0])

    return t_ang * 180. / 3.1415

