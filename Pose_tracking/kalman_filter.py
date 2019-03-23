import math
import numpy
from core.agent import Robot
from Pose_tracking.sensor_model import Sensor


class Kalman:

    def __init__(self, robo):
        self.robo = robo
        self.mu = numpy.matrix([[self.robo.x], [self.robo.y], [self.robo.theta]])
        self.u = numpy.matrix([[self.robo.v], [self.robo.w]])
        self.mu_out = numpy.zeros((3, 1))
        self.sigma_out = numpy.zeros((3, 3))
        self.sigma = numpy.diag((0.1e-5, 0.1e-5, 0.1e-5))
        self.A = numpy.identity(3)
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.robo.theta), 0], \
                            [Robot.DELTA_T * math.sin(self.robo.theta), 0], \
                            [0, Robot.DELTA_T]])
        self.R = numpy.matrix([[numpy.var(0.01), 0, 0], [0, numpy.var(0.01), 0], [0, 0, numpy.var(0.01)]])  # covariance matrix
        self.C = numpy.identity(3)
        self.sigma_t = numpy.zeros((3, 3))
        self.I = numpy.identity(3)
        self.Q = numpy.matrix([[numpy.var(0.01), 0, 0], [0, numpy.var(0.01), 0], [0, 0, numpy.var(0.01)]])
        self.z = numpy.zeros((3, 1))
        self.gaussian_noise = numpy.matrix([[numpy.random.normal(0, 1)], [numpy.random.normal(0, 15)], [numpy.random.normal(0, 15)]])

    def prediction(self):
        self.mu_out = self.A * self.mu + self.B * self.u
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(self.mu[2]), 0], \
                            [Robot.DELTA_T * math.sin(self.mu[2]), 0], \
                            [0, Robot.DELTA_T]])
        self.sigma_out = self.A * self.sigma * numpy.transpose(self.A) \
            + self.R

    def correction(self):
        #TODO: correct update of landmark_x and y(position x and y of landmark),
        #TODO: distance to landmarks, bearing(angle to landmark)
        sensor: Sensor = Sensor(self.mu[2], 3, 2, 5, 20, 1)
        sensor.feature_based_measurement()

        #TODO: update sigma correctly
        self.sigma = numpy.diag(
            (numpy.var(sensor.estimated_x), numpy.var(sensor.estimated_y), numpy.var(sensor.estimated_theta)))

        K = self.sigma_out * numpy.transpose(self.C) * numpy.linalg.inv(self.C * self.sigma_out * numpy.transpose(self.C) + self.Q)
        self.z = numpy.matrix([[sensor.estimated_x], [sensor.estimated_y], [sensor.estimated_theta]]) + self.gaussian_noise
        self.mu = self.mu_out + K * (self.z - self.C * self.mu_out)
        self.sigma_t = (self.I - K * self.C) * self.sigma_out

        print('covariance' + str(self.sigma))
        print('mu' + str(self.mu))
        print('real x = ' + str(self.robo.x) + ', real y = ' + str(self.robo.y) + ', real theta = ' + str(self.robo.theta))

