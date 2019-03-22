import math
import numpy
from PyQt5.QtGui import QPainterPath

from core.map import Map
from settings import SETTINGS


class Robot:
    SPEED_INCREMENT = 0.3
    SPEED_DECREMENT = 0.3
    ANGLE_INCREMENT = 0.1
    ANGLE_DECREMENT = 0.1
    DELTA_T = SETTINGS["DELTA_T"]

    def __init__(self, radius: int, map: Map, x=0, y=0):
        self.radius = radius
        self.diameter = radius * 2
        self.x = x
        self.y = y
        self.v = 0
        self.w = 0
        self.theta = 0

        self.trace = []

        self.map = map

    def increment_v(self):
        self.v = self.v + Robot.SPEED_INCREMENT

    def decrement_v(self):
        self.v = self.v - Robot.SPEED_DECREMENT

    def increment_w(self):
        self.w = self.w + Robot.ANGLE_INCREMENT

    def decrement_w(self):
        self.w = self.w - Robot.ANGLE_DECREMENT

    def stop(self):
        self.v = 0
        self.w = 0

    def velocity_based_model(self):
        out = numpy.matrix([[self.x], [self.y], [self.theta]]) \
            + numpy.matrix([[Robot.DELTA_T * math.cos(self.theta), 0], \
                            [Robot.DELTA_T * math.sin(self.theta), 0], \
                            [0, Robot.DELTA_T]])  \
            * numpy.matrix([[self.v], [self.w]])
        self.x = out[0, 0]
        self.y = out[1, 0]
        self.theta = out[2, 0]

    def get_beacon_distances(self):
        return self.map.get_beacon_distances(self.x, self.y)


if __name__ == "__main__":
    import pygame
    from pygame import gfxdraw

    pygame.init()  # initialize pygame
    pygame.font.init()

    display_width = 1000
    display_height = 700
    border_padding = 20

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    lightblue = (66, 134, 244)

    robo_color = red

    robi: Robot = Robot(20, x=100, y=100)

    game_display = pygame.display.set_mode((display_width, display_height))  # size of environment
    pygame.display.set_caption('Mobile Robot Simulator')
    clock = pygame.time.Clock()

    step = 0
    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        # CONTROL
        keys_pressed = pygame.key.get_pressed()
        # INCREMENT v
        if keys_pressed[pygame.K_w]:
            robi.increment_v()
        # INCREMENT w
        if keys_pressed[pygame.K_d]:
            robi.increment_w()

        # DECREMENT v
        if keys_pressed[pygame.K_s]:
            robi.decrement_v()
        # DECREMENT w
        if keys_pressed[pygame.K_a]:
            robi.decrement_w()

        # STOP
        if keys_pressed[pygame.K_x]:
            robi.stop()

        robi.velocity_based_model()

        # ROBOT SHAPE LOCATIONS
        robot_center_x = int(round(robi.x))
        robot_center_y = int(round(robi.y))
        robot_nose_x = int(robi.x + (robi.radius * math.cos(robi.theta)))
        robot_nose_y = int(robi.y + (robi.radius * math.sin(robi.theta)))

        # DRAW ENVIRONMENT
        game_display.fill(white)

        # DRAW ROBOT
        gfxdraw.aacircle(game_display, robot_center_x, robot_center_y, robi.radius, black)
        gfxdraw.line(game_display, robot_center_x, robot_center_y, robot_nose_x, robot_nose_y, black)

        pygame.display.update()

        step += 1

    pygame.quit()
    quit()
