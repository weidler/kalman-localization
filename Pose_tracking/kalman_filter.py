import math
import numpy
from core.agent import robi


class Kalman:

    def __init__(self):
        self.mü = numpy.matrix([[robi.x], [robi.y], [robi.theta]])
        self.mü_out = numpy.zeros((3, 1))
        self.sigma_out = numpy.zeros(3, 3)
        self.R = numpy.matrix([[numpy.var(0.01), 0, 0], [0, numpy.var(0.01), 0], [0, 0, numpy.var(0.01)]])  # covariance matrix
        self.K = numpy.zeros(3, 3)
        self.C = numpy.zeros(3, 3)
        self.mü_t = numpy.zeros((3, 1))
        self.sigma_t = numpy.zeros(3, 3)
        self.I = numpy.identity(3)

    def prediction(self):
        self.mü_out = self.mü * robi.A + robi.B * robi.u
        self.sigma_out = robi.A * self.sigma * numpy.transpose(robi.A) \
            + self.R

    def correction(self):
        self.K = self.sigma_out * numpy.transpose(self.C) * numpy.linalg.inv(self.C * self.sigma_out * numpy.transpose(self.C) + self.Q)
        self.mü_t = self.mü_out + self.K * (self.z - self.C * self.mü_out)
        self.sigma_t = (self.I - self.K * self.C) * self.sigma_out

