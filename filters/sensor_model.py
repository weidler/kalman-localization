from numpy import *


def feature_based_measurement(theta, mx, my, distance, bearing, x_pred, y_pred):
    x = mx - math.cos(theta - bearing) * distance
    y = my - math.sin(theta - bearing) * distance

    return x, y, theta
