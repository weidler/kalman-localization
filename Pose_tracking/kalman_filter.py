import math
import numpy
from core.agent import Robot


class Kalman:

    def __init__(self, v, w, init_x, init_y, init_theta):
        self.v = v
        self.w = w
        self.mu = numpy.matrix([[init_x], [init_y], [init_theta]])
        self.u = numpy.matrix([[self.v], [self.w]])
        self.mu_out = numpy.zeros((3, 1))
        self.sigma_out = numpy.zeros((3, 3))
        self.sigma = numpy.diag((0.01, 0.01, 0.01))
        self.A = numpy.identity(3)
        self.B = numpy.matrix([[Robot.DELTA_T * math.cos(init_theta), 0], \
                            [Robot.DELTA_T * math.sin(init_theta), 0], \
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
        self.sigma = numpy.diag((numpy.var(estimated_x), numpy.var(estimated_y), numpy.var(estimated_theta)))

    def correction(self, robo):
        K = self.sigma_out * numpy.transpose(self.C) * numpy.linalg.inv(self.C * self.sigma_out * numpy.transpose(self.C) + self.Q)
        self.z = numpy.matrix([[estimated_x], [estimated_y], [estimated_theta]]) + self.gaussian_noise
        self.mu = self.mu_out + K * (self.z - self.C * self.mu_out)
        self.sigma_t = (self.I - K * self.C) * self.sigma_out

        print('K = ' + str(K))
        print('mü = ' + str(self.mu) + ' ' + 'sigma = ' + str(self.sigma_t))
        print('real x = ' + str(robo.x) + ' ' + 'real y = ' + str(robo.y) + ' ' + 'real theta = ' + str(robo.theta))
