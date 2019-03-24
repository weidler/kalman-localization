from numpy import *
from scipy.optimize import *


def feature_based_measurement(mu, landmark_position_x, landmark_position_y, distance, bearing, signature):

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
        f[0] = math.sqrt((landmark_position_x - x) ** 2 + (landmark_position_y - y) ** 2) - distance
        f[1] = math.atan2(landmark_position_y - y, landmark_position_x - x) - mu - bearing
        return f

    z_guess = array([500, 500])
    z = fsolve(equations, z_guess)

    estimated_x = z[0]
    estimated_y = z[1]
    estimated_theta = mu

    return estimated_x, estimated_y, estimated_theta
