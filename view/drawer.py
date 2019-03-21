from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QPainterPath

from core.agent import Robot
from core.map import Map
from settings import SETTINGS

import math


def draw_robot(painter: QPainter, robot: Robot):
    robot_nose_x = int(robot.x + (robot.radius * math.cos(robot.theta)))
    robot_nose_y = int(robot.y + (robot.radius * math.sin(robot.theta)))

    pen = QPen()
    pen.setStyle(Qt.DashLine)
    pen.setBrush(SETTINGS["COLOR_ROBOT"].darker())
    pen.setWidth(3)
    brush = SETTINGS["COLOR_ROBOT"]

    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawEllipse(QPoint(robot.x, robot.y), robot.radius, robot.radius)
    pen.setStyle(Qt.SolidLine)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.drawLine(robot.x, robot.y, robot_nose_x, robot_nose_y)


def draw_beacons(painter: QPainter, map: Map):
    pen = QPen()
    pen.setBrush(SETTINGS["COLOR_BEACON"])
    pen.setWidth(6)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)

    for beacon in map.beacons:
        painter.drawPoint(beacon.x, beacon.y)


def draw_beacon_indicators(painter: QPainter, map: map, robot: Robot):
    pen = QPen()
    pen.setStyle(Qt.DotLine)
    pen.setCapStyle(Qt.RoundCap)
    pen.setBrush(SETTINGS["COLOR_BEACON"])
    pen.setWidth(3)
    painter.setPen(pen)

    for beacon in map.beacons:
        if beacon.distance_to(robot.x, robot.y) <= SETTINGS["BEACON_INDICATOR_DISTANCE"]:
            painter.drawLine(beacon.x, beacon.y, robot.x, robot.y)


def draw_trace(painter: QPainter, trace: QPainterPath):
    pen = QPen()
    pen.setStyle(Qt.SolidLine)
    pen.setBrush(SETTINGS["COLOR_TRACE"])
    pen.setWidth(2)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)

    painter.drawPath(trace)