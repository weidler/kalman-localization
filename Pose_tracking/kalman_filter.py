import math
import statistics
import numpy

from Pose_tracking.sensor_model import feature_based_measurement
from core.agent import Robot
from settings import SETTINGS


class Kalman:

    def __init__(self, robo: Robot):
        self.robo: Robot = robo
        self.u = numpy.matrix([[0], [0]], dtype='float')
        self.mu = numpy.matrix([[self.robo.x], [self.robo.y], [self.robo.theta]], dtype='float')
        self.mu_out = numpy.zeros((3, 1))
        self.sigma = numpy.diag((SETTINGS["VERY_SMALL_NUMBER"], SETTINGS["VERY_SMALL_NUMBER"], SETTINGS["VERY_SMALL_NUMBER"]))
        self.sigma_out = self.sigma.copy()
        self.A = numpy.identity(3)
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.robo.theta), 0],
                               [Robot.DELTA_T * math.sin(self.robo.theta), 0],
                               [0, Robot.DELTA_T]], dtype='float')
        self.R = numpy.matrix(
            [[SETTINGS["VERY_SMALL_NUMBER"], 0, 0], [0, SETTINGS["VERY_SMALL_NUMBER"], 0], [0, 0, SETTINGS["VERY_SMALL_NUMBER"]]],
            dtype='float')  # covariance matrix

        self.C = numpy.identity(3)
        self.sigma_t = self.sigma.copy()
        self.I = numpy.identity(3)
        self.Q = numpy.matrix([[SETTINGS["VERY_SMALL_NUMBER"], 0, 0], [0, SETTINGS["VERY_SMALL_NUMBER"], 0], [0, 0, SETTINGS["VERY_SMALL_NUMBER"]]],
                              dtype='float')
        self.z = numpy.zeros((3, 1))
        self.K = numpy.zeros((3, 3))
        self.gaussian_noise = numpy.matrix(
            [[numpy.random.normal(0, 1)], [numpy.random.normal(0, 1)], [numpy.random.normal(0, 1)]], dtype='float')

    def prediction(self):
        self.u = numpy.matrix([[self.robo.v], [self.robo.w]], dtype='float')
        self.mu_out = self.A * self.mu + self.B * self.u
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.mu[2]), 0],
                               [Robot.DELTA_T * math.sin(self.mu[2]), 0],
                               [0, Robot.DELTA_T]], dtype='float')
        self.sigma_out = self.A * self.sigma * numpy.transpose(self.A) \
                         + self.R
        # self.R = statistics.stdev()

    def correction(self):
        # TODO: correct update of landmark_x and y(position x and y of landmark),
        # TODO: distance to landmarks, bearing(angle to landmark)

        n_landmarks = len(self.robo.map.beacons)
        total_estimated_x, total_estimated_y, total_estimated_theta = 0, 0, 0
        for i, beacon in enumerate(
                self.robo.map.get_beacons_in_distance(self.robo.x, self.robo.y, SETTINGS["BEACON_INDICATOR_DISTANCE"])):
            estimated_x, estimated_y, estimated_theta = feature_based_measurement(self.mu[2], beacon.x, beacon.y,
                                                                                  beacon.distance_to(self.robo.x,
                                                                                                     self.robo.y),
                                                                                  beacon.bearing(self.robo.x,
                                                                                                 self.robo.y,
                                                                                                 self.robo.theta),
                                                                                  i)
            total_estimated_x += estimated_x
            total_estimated_y += estimated_y
            total_estimated_theta += estimated_theta

        estimated_x, estimated_y, estimated_theta = total_estimated_x / n_landmarks, \
                                                    total_estimated_y / n_landmarks, \
                                                    total_estimated_theta / n_landmarks

        # TODO: update sigma correctly
        self.sigma = numpy.diag(
            (numpy.var(estimated_x), numpy.var(estimated_y), numpy.var(estimated_theta)))
        inverse = self.C * self.sigma_out * numpy.transpose(self.C) + self.Q
        numpy.linalg.det(inverse)
        self.K = self.sigma_out * numpy.transpose(self.C) * numpy.linalg.pinv(inverse)
        self.z = numpy.matrix(
            [[estimated_x], [estimated_y], [estimated_theta]], dtype='float') + self.gaussian_noise
        self.mu = self.mu_out + self.K * (self.z - self.C * self.mu_out)
        self.sigma_t = (self.I - self.K * self.C) * self.sigma_out

        # print('covariance' + str(self.sigma_t))
        # print('mu' + str(self.mu))
        # print('real x = ' + str(self.robo.x) + ', real y = ' + str(self.robo.y) + ', real theta = ' + str(self.robo.theta))
