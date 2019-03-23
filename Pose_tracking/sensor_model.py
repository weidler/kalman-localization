from numpy import *
from scipy.optimize import *


class Sensor:

    def __init__(self, mu, landmark_position_x, landmark_position_y, distance, bearing, signature):
        self.mu = mu
        self.landmark_position_x = landmark_position_x
        self.landmark_position_y = landmark_position_y
        self.distance = distance
        self.bearing = bearing
        self.signature = signature
        self.estimated_x = 0
        self.estimated_y = 0
        self.estimated_theta = 0

    def feature_based_measurement(self):

        # Example: non-linear equation (https://stackoverflow.com/questions/8739227/how-to-solve-a-pair-of-nonlinear-equations-using-python)
        # def equations(p):
        #     x, y = p
        #     return x+y**2-4, math.exp(x) + x*y - 3
        #
        # x, y =  fsolve(equations, (1, 1))
        #
        # print equations((x, y))

        # TODO: add gaussian noise
        def equations(z):
            x = z[0]
            y = z[1]

            f = empty(2)
            f[0] = math.sqrt((self.landmark_position_x - x) ** 2 + (self.landmark_position_y - y) ** 2) - self.distance
            f[1] = math.atan2(self.landmark_position_y - y, self.landmark_position_x - x) - self.mu - self.bearing
            return f

        z_guess = array([50, 50])
        z = fsolve(equations, z_guess)

        self.estimated_x = z[0]
        self.estimated_y = z[1]
        self.estimated_theta = self.mu


