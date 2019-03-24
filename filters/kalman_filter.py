import math

import numpy

from filters.sensor_model import feature_based_measurement
from core.agent import Robot
from settings import SETTINGS

from numpy.random import uniform as uni

numpy.random.seed(10000)

class Kalman:

    def __init__(self, robot: Robot):
        self.robot: Robot = robot
        self.step_counter = 0

        # STATE MU
        self.mu = numpy.matrix([[self.robot.x], [self.robot.y], [self.robot.theta]], dtype='float')
        self.mu_prediction = self.mu.copy()

        # MOTION MODEL VALUES
        self.u = numpy.matrix([[self.robot.v], [self.robot.w]], dtype='float')

        # STATE COVARIANCE ESTIMATE
        self.sigma = numpy.diag((0.0001,
                                 0.0001,
                                 0.0001))
        self.sigma_prediction = self.sigma.copy()

        # UNCONTROLLED TRANSITION MATRIX A
        self.A = numpy.identity(3)

        # CONTROL TRANSITION MATRIX B
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.robot.theta), 0],
                               [Robot.DELTA_T * -math.sin(self.robot.theta), 0],
                               [0, Robot.DELTA_T]], dtype='float')

        # MOTION NOISE
        self.R = numpy.matrix([[uni(0, SETTINGS["MOTION_NOISE"]), 0, 0],
                               [0, uni(0, SETTINGS["MOTION_NOISE"]), 0],
                               [0, 0, uni(0, SETTINGS["MOTION_NOISE"])]], dtype='float')

        # MAPPING STATES TO OBSERVATIONS
        self.C = numpy.identity(3)

        # IDENTITY MATRIX
        self.I = numpy.identity(3)

        # SENSOR NOISE
        self.Q = numpy.matrix([[uni(0, SETTINGS["SENSOR_NOISE"]), 0, 0],
                               [0, uni(0, SETTINGS["SENSOR_NOISE"]), 0],
                               [0, 0, uni(0, SETTINGS["SENSOR_NOISE"])]], dtype='float')

        # STATE ESTIMATED FROM SENSOR DATA
        self.z = numpy.zeros((3, 1))

        # KALMAN GAIN
        self.K = numpy.zeros((3, 3))

    @staticmethod
    def delta():
        return numpy.matrix([[numpy.random.normal(0, SETTINGS["SENSOR_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["SENSOR_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["SENSOR_NOISE"])]], dtype='float')

    @staticmethod
    def epsilon():
        return numpy.matrix([[numpy.random.normal(0, SETTINGS["MOTION_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["MOTION_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["MOTION_NOISE"])]], dtype='float')

    def prediction(self):
        # update u
        self.u = numpy.matrix([[self.robot.v], [self.robot.w]], dtype='float')

        # update B
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.mu[2]), 0],
                               [Robot.DELTA_T * math.sin(self.mu[2]), 0],
                               [0, Robot.DELTA_T]], dtype='float')

        # estimate mu based on motion model, TODO noise
        self.mu_prediction = self.A * self.mu + self.B * self.u + self.epsilon()

        # estimate sigma
        self.sigma_prediction = self.A * self.sigma * numpy.transpose(self.A) + self.R
        self.step_counter += 1

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
        self.z = numpy.matrix([[total_estimated_x / (n_landmarks or 1)],
                               [total_estimated_y / (n_landmarks or 1)],
                               [total_estimated_theta / (n_landmarks or 1)]], dtype='float') + self.delta()

        inverse = numpy.linalg.pinv(self.C * self.sigma_prediction * self.C.transpose() + self.Q)
        # K is the influence of the difference between measurement and prediction
        K = self.sigma_prediction * self.C.transpose() * inverse
        print(K.sum()/3)
        self.mu = self.mu_prediction + K * (self.z - self.C * self.mu_prediction)
        self.sigma = (self.I - self.K * self.C) * self.sigma_prediction

        return self.mu
