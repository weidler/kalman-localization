import math

import numpy
from PyQt5.QtGui import QPainterPath
from core.map import Map
from settings import SETTINGS


class Robot:
    SPEED_INCREMENT = 1
    SPEED_DECREMENT = 1
    ANGLE_INCREMENT = 0.1
    ANGLE_DECREMENT = 0.1
    DELTA_T = SETTINGS["DELTA_T"]

    def __init__(self, radius: int, map: Map):
        self.radius = radius
        self.diameter = radius * 2
        self.x = map.start_x
        self.y = map.start_y
        self.v = 0
        self.w = 0
        self.theta = math.radians(90)

        self.map: Map = map

        self.fixed_motion_noise = numpy.matrix([[numpy.random.normal(0, SETTINGS["V_NOISE"])],
                                                [numpy.random.normal(0, SETTINGS["W_NOISE"])]], dtype='float')

        self.trace = []

    def increment_v(self):
        self.v = self.v + Robot.SPEED_INCREMENT

    def decrement_v(self):
        self.v = self.v - Robot.SPEED_DECREMENT

    def increment_w(self):
        self.w = self.w + Robot.ANGLE_INCREMENT

    def decrement_w(self):
        self.w = self.w - Robot.ANGLE_DECREMENT

    def stop(self):
        self.v = 0
        self.w = 0

    def velocity_based_model(self):
        self.theta = self.theta % (2 * math.pi)
        out = numpy.matrix([[self.x], [self.y], [self.theta]]) + numpy.matrix(
            [[Robot.DELTA_T * math.cos(self.theta), 0], [Robot.DELTA_T * math.sin(self.theta), 0],
             [0, Robot.DELTA_T]]) * (numpy.matrix([[self.v], [self.w]] + self.fixed_motion_noise))
        self.x = out[0, 0]
        self.y = out[1, 0]
        self.theta = out[2, 0]

    def get_beacon_info(self):
        return list(
            zip(self.map.get_bearings(self.x, self.y, self.theta), self.map.get_beacon_distances(self.x, self.y)))
