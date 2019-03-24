import math
import numpy
import pygame

from pygame import gfxdraw

from core.agent import Robot
from filters.kalman_filter import Kalman
from core.map import Map

if __name__ == "__main__":
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

    robi: Robot = Robot(40, Map(display_width, display_height))
    kalman: Kalman = Kalman(robi)

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
        kalman.prediction()
        kalman.correction()

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
