import numpy
import math

def feature_based_measurement(theta, mx, my, distance, bearing, distance_noise, bearing_noise):
    distance += distance_noise
    bearing += bearing_noise

    x = mx - math.cos(theta - bearing) * distance
    y = my - math.sin(theta - bearing) * distance

    return x, y, theta
