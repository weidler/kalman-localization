import math

import numpy

from filters.sensor_model import feature_based_measurement
from core.agent import Robot
from settings import SETTINGS


class Kalman:

    def __init__(self, robot: Robot):
        self.robot: Robot = robot

        # STATE MU
        self.mu = numpy.matrix([[self.robot.x], [self.robot.y], [self.robot.theta]], dtype='float')
        self.mu_prediction = self.mu.copy()

        # MOTION MODEL VALUES
        self.u = numpy.matrix([[self.robot.v], [self.robot.w]], dtype='float')

        # STATE COVARIANCE ESTIMATE
        self.sigma = numpy.diag((SETTINGS["VERY_SMALL_NUMBER"],
                                 SETTINGS["VERY_SMALL_NUMBER"],
                                 SETTINGS["VERY_SMALL_NUMBER"]))
        self.sigma_prediction = self.sigma.copy()

        # UNCONTROLLED TRANSITION MATRIX A
        self.A = numpy.identity(3)

        # CONTROL TRANSITION MATRIX B
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.robot.theta), 0],
                               [Robot.DELTA_T * math.sin(self.robot.theta), 0],
                               [0, Robot.DELTA_T]], dtype='float')

        # NOISE
        self.R = numpy.matrix([[SETTINGS["VERY_SMALL_NUMBER"], 0, 0],
                               [0, SETTINGS["VERY_SMALL_NUMBER"], 0],
                               [0, 0, SETTINGS["VERY_SMALL_NUMBER"]]], dtype='float')

        # MAPPING STATES TO OBSERVATIONS
        self.C = numpy.identity(3)

        # IDENTITY MATRIX
        self.I = numpy.identity(3)

        # SENSOR NOISE COVARIANCE MATRIX
        self.Q = numpy.matrix([[SETTINGS["VERY_SMALL_NUMBER"], 0, 0],
                               [0, SETTINGS["VERY_SMALL_NUMBER"], 0],
                               [0, 0, SETTINGS["VERY_SMALL_NUMBER"]]], dtype='float')

        # STATE ESTIMATED FROM SENSOR DATA
        self.z = numpy.zeros((3, 1))

        # KALMAN GAIN
        self.K = numpy.zeros((3, 3))
        self.gaussian_noise = numpy.matrix([[numpy.random.normal(0, 0.01)],
                                            [numpy.random.normal(0, 0.01)],
                                            [numpy.random.normal(0, 0.01)]], dtype='float')

    def prediction(self):
        # update u
        self.u = numpy.matrix([[self.robot.v], [self.robot.w]], dtype='float')

        # update B
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.mu[2]), 0],
                               [Robot.DELTA_T * math.sin(self.mu[2]), 0],
                               [0, Robot.DELTA_T]], dtype='float')

        # estimate mu based on motion model
        self.mu_prediction = self.A * self.mu + self.B * self.u

        # estimate sigma
        self.sigma_prediction = self.A * self.sigma * numpy.transpose(self.A) + self.R

        return self.mu_prediction

    def correction(self):
        # measure landmarks and estimate x, y, theta
        in_range_beacons = self.robot.map.get_beacons_in_distance(self.robot.x, self.robot.y, SETTINGS["BEACON_INDICATOR_DISTANCE"])
        n_landmarks = len(in_range_beacons)
        total_estimated_x, total_estimated_y, total_estimated_theta = 0, 0, 0
        for i, beacon in enumerate(in_range_beacons):
            estimated_x, estimated_y, estimated_theta = feature_based_measurement(int(self.mu[2]),
                                                                                  beacon.x,
                                                                                  beacon.y,
                                                                                  beacon.distance_to(self.robot.x,
                                                                                                     self.robot.y),
                                                                                  beacon.bearing(self.robot.x,
                                                                                                 self.robot.y,
                                                                                                 self.robot.theta),
                                                                                  self.mu_prediction[0, 0],
                                                                                  self.mu_prediction[1, 0])
            total_estimated_x += estimated_x
            total_estimated_y += estimated_y
            total_estimated_theta += estimated_theta

        # average over landmarks
        self.z = numpy.matrix([[total_estimated_x / n_landmarks],
                               [total_estimated_y / n_landmarks],
                               [total_estimated_theta / n_landmarks]], dtype='float') + self.gaussian_noise

        inverse = numpy.linalg.inv(self.C * self.sigma_prediction * self.C.transpose() + self.Q)
        self.K = self.sigma_prediction * self.C.transpose() * inverse
        self.mu = self.mu_prediction + self.K * (self.z - self.C * self.mu_prediction)
        self.sigma = (self.I - self.K * self.C) * self.sigma_prediction

        return self.z

        # print('covariance' + str(self.sigma))
        # print('mu' + str(self.mu))
        # print('real x = ' + str(self.robo.x) + ', real y = ' + str(self.robo.y) + ', real theta = ' + str(self.robo.theta))
