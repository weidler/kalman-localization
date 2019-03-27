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

        # STATE MU
        self.mu = numpy.matrix([[self.robot.x], [self.robot.y], [self.robot.theta]], dtype='float')
        self.mu_prediction = self.mu.copy()

        # MOTION MODEL VALUES
        self.u = numpy.matrix([[self.robot.v], [self.robot.w]], dtype='float')

        # STATE COVARIANCE ESTIMATE
        self.sigma = numpy.diag((SETTINGS["INITIAL_COVARIANCE"],
                                 SETTINGS["INITIAL_COVARIANCE"],
                                 SETTINGS["INITIAL_COVARIANCE"]))
        self.sigma_prediction = self.sigma.copy()

        # UNCONTROLLED TRANSITION MATRIX A
        self.A = numpy.identity(3)

        # CONTROL TRANSITION MATRIX B
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.robot.theta), 0],
                               [Robot.DELTA_T * math.sin(self.robot.theta), 0],
                               [0, Robot.DELTA_T]], dtype='float')

        # MOTION NOISE ESTIMATION
        self.R = numpy.matrix([[uni(0, SETTINGS["MOTION_NOISE_ESTIMATION"]), 0, 0],
                               [0, uni(0, SETTINGS["MOTION_NOISE_ESTIMATION"]), 0],
                               [0, 0, uni(0, SETTINGS["MOTION_NOISE_ESTIMATION"])]], dtype='float')

        # MAPPING STATES TO OBSERVATIONS
        self.C = numpy.identity(3)

        # IDENTITY MATRIX
        self.I = numpy.identity(3)

        # SENSOR NOISE ESTIMATION
        self.Q = numpy.matrix([[uni(0, SETTINGS["SENSOR_NOISE_ESTIMATION"]), 0, 0],
                               [0, uni(0, SETTINGS["SENSOR_NOISE_ESTIMATION"]), 0],
                               [0, 0, uni(0, SETTINGS["SENSOR_NOISE_ESTIMATION"])]], dtype='float')

        # STATE ESTIMATED FROM SENSOR DATA
        self.z = numpy.zeros((3, 1))

        # KALMAN GAIN
        self.K_trace = [0]

    @staticmethod
    def epsilon():
        return numpy.matrix([[numpy.random.normal(0, SETTINGS["MOTION_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["MOTION_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["MOTION_THETA_NOISE"])]], dtype='float')

    @staticmethod
    def delta():
        return numpy.matrix([[numpy.random.normal(0, SETTINGS["SENSOR_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["SENSOR_NOISE"])],
                             [numpy.random.normal(0, SETTINGS["SENSOR_NOISE"])]], dtype='float')

    def prediction(self):
        # update u
        self.u = numpy.matrix([[self.robot.v], [self.robot.w]], dtype='float')

        # update B
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.mu[2]), 0],
                               [Robot.DELTA_T * math.sin(self.mu[2]), 0],
                               [0, Robot.DELTA_T]], dtype='float')

        # estimate mu based on motion model
        self.mu_prediction = self.A * self.mu + self.B * self.u + self.epsilon()

        # estimate sigma
        self.sigma_prediction = self.A * self.sigma * numpy.transpose(self.A) + self.R

        return self.mu_prediction

    def correction(self):
        # measure landmarks and estimate x, y, theta
        in_range_beacons = self.robot.map.get_beacons_in_distance(self.robot.x, self.robot.y, SETTINGS["BEACON_INDICATOR_DISTANCE"])
        n_landmarks = len(in_range_beacons)
        total_estimated_x, total_estimated_y, total_estimated_theta = 0, 0, 0
        for i, beacon in enumerate(in_range_beacons):
            estimated_x, estimated_y, estimated_theta = feature_based_measurement(self.mu_prediction[2, 0],
                                                                                  beacon.x,
                                                                                  beacon.y,
                                                                                  beacon.distance_to(self.robot.x,
                                                                                                     self.robot.y),
                                                                                  beacon.bearing(self.robot.x,
                                                                                                 self.robot.y,
                                                                                                 self.robot.theta))

            noise = self.delta()

            total_estimated_x += estimated_x + noise[0, 0]
            total_estimated_y += estimated_y + noise[1, 0]
            total_estimated_theta += estimated_theta

        # average over landmarks
        self.z = numpy.matrix([[total_estimated_x / (n_landmarks or 1)],
                               [total_estimated_y / (n_landmarks or 1)],
                               [total_estimated_theta / (n_landmarks or 1)]], dtype='float')

        # this is essentially the inverse of the predicted sigma + Q
        # that is Sigma + R + Q
        inverse = numpy.linalg.pinv(self.C * self.sigma_prediction * self.C.transpose() + self.Q)
        # K is the influence of the difference between measurement and prediction
        K = self.sigma_prediction * self.C.transpose() * inverse
        self.K_trace.append(K.sum()/3)

        if n_landmarks == 0:
            K = 0

        self.mu = self.mu_prediction + K * (self.z - self.C * self.mu_prediction)
        self.sigma = (self.I - K * self.C) * self.sigma_prediction

        return self.mu
