import math
import numpy
from core.agent import Robot


class Kalman:

    def __init__(self, v, w):
        self.v = v
        self.w = w
        self.u = numpy.matrix([[self.v], [self.w]])
        self.mü = numpy.zeros((3, 1))
        self.mü_out = numpy.zeros((3, 1))
        self.sigma_out = numpy.zeros((3, 3))
        self.sigma = numpy.zeros((3, 3))
        self.A = numpy.identity(3)
        self.B = numpy.zeros((3, 2))
        self.R = numpy.matrix([[numpy.var(0.01), 0, 0], [0, numpy.var(0.01), 0], [0, 0, numpy.var(0.01)]])  # covariance matrix
        self.C = numpy.identity(3)
        self.mü_t = numpy.zeros((3, 1))
        self.sigma_t = numpy.zeros((3, 3))
        self.I = numpy.identity(3)
        self.Q = numpy.matrix([[numpy.var(0.01), 0, 0], [0, numpy.var(0.01), 0], [0, 0, numpy.var(0.01)]])
        self.z = numpy.zeros((3, 1))
        self.gaussian_noise = numpy.matrix([[numpy.random.normal(0, 1)], [numpy.random.normal(0, 1)], [numpy.random.normal(0, 1)]])

    def prediction(self, robo):
        self.mü = numpy.matrix([[robo.x], [robo.y], [robo.theta]])
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(robo.theta), 0], \
                            [Robot.DELTA_T * math.sin(robo.theta), 0], \
                            [0, Robot.DELTA_T]])
        self.mü_out = self.A * self.mü + self.B * self.u
        self.sigma = numpy.diag((0.01, 0.01, 0.01))
        self.sigma_out = self.A * self.sigma * numpy.transpose(self.A) \
            + self.R

    def correction(self, robo):
        K = self.sigma_out * numpy.transpose(self.C) * numpy.linalg.inv(self.C * self.sigma_out * numpy.transpose(self.C) + self.Q)
        self.z = numpy.matrix([[robo.x], [robo.y], [robo.theta]]) + self.gaussian_noise
        self.mü_t = self.mü_out + K * (self.z - self.C * self.mü_out)
        self.sigma_t = (self.I - K * self.C) * self.sigma_out

        print('mü = ' + str(self.mü_t) + ' ' + 'sigma = ' + str(self.sigma_t))
