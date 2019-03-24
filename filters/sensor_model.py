import numpy

from numpy import *
from scipy.optimize import *

from sympy.core.symbol import symbols
from sympy.solvers.solveset import nonlinsolve
import sympy

from settings import SETTINGS


def feature_based_measurement(theta, mx, my, distance, bearing, x_pred, y_pred):
    # TODO: add gaussian noise
    # def equations(z):
    #     x = z[0]
    #     y = z[1]
    #
    #     f = empty(2)
    #     f[0] = math.sqrt((mx - x) ** 2 + (my - y) ** 2) - distance
    #     f[1] = math.atan2(my - y, mx - x) - theta - bearing
    #
    #     return f
    #
    # z_guess = array([x_pred, y_pred])
    # z = fsolve(equations, z_guess)
    # x, y = z[0], z[1]

    # x, y = symbols("x, y", real=True)
    # system = [sympy.sqrt((mx - x) ** 2 + (my - y) ** 2) - distance,
    #           sympy.atan2(my - y, mx - x) - theta - bearing]
    #
    # z = nonlinsolve(system, [x, y])
    #
    # eps = 0.001
    # t = math.tan(bearing + theta - eps)**2
    # a = my
    # b = mx
    # r = distance
    #
    # # y = (-sqrt(-(a**2)*(t**4) + 2*a*b*(t**4) - (b**2)*(t**4) + (eps**2)*(t**2) - 2*eps*r*(t**4) - 2*eps*r*(t**2) + (r**2)*(t**4) + (r**2)*(t**2) + a*(t**2) - a*t + a + b*t))/((t**2) + 1)
    # # x = - sqrt((r - eps)**2 - (a - y)**2) + b
    #
    # y = my - math.sqrt((r - eps)**2 / ((1/t) + 1))
    # x = - math.sqrt((r - eps) ** 2 - (my - y) ** 2) + mx

    x = mx - math.cos(bearing - theta) * distance
    y = my + math.sin(bearing - theta) * distance

    return x, y, theta
