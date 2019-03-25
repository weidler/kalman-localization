import math

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt, QRectF
from PyQt5.QtGui import QPainter, QPen, QPainterPath, QFont, QBrush, QImage

from core.agent import Robot
from settings import SETTINGS


def draw_robot(painter: QPainter, robot: Robot):
    robot_nose_x = int(robot.x + (robot.radius * math.cos(robot.theta)))
    robot_nose_y = int(robot.y + (robot.radius * math.sin(robot.theta)))

    brush = SETTINGS["COLOR_ROBOT"]

    pen = QPen()
    pen.setStyle(Qt.SolidLine)
    pen.setBrush(SETTINGS["COLOR_ROBOT"].darker())
    pen.setWidth(2)

    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawEllipse(QPoint(robot.x, robot.y), robot.radius, robot.radius)
    pen.setStyle(Qt.SolidLine)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.drawLine(robot.x, robot.y, robot_nose_x, robot_nose_y)


def draw_beacons(painter: QPainter, robot: Robot):
    pen = QPen()
    pen.setBrush(SETTINGS["COLOR_BEACON"])
    pen.setWidth(SETTINGS["BEACON_SIZE"])
    pen.setCapStyle(Qt.RoundCap)

    hint_font = QFont()
    hint_font.setPointSize(10)
    painter.setFont(hint_font)

    for beacon in robot.map.beacons:
        if beacon.distance_to(robot.x, robot.y) <= SETTINGS["BEACON_INDICATOR_DISTANCE"]:
            painter.drawText(QRectF(beacon.x + 20, beacon.y - 20, 40, 40), Qt.AlignCenter,
                             f"{round(math.degrees(beacon.bearing(robot.x, robot.y, robot.theta)))}°\n"
                             f"{round(beacon.distance_to(robot.x, robot.y))}u")
            pen.setWidth(SETTINGS["BEACON_SIZE"] * 1.5)
        else:
            pen.setWidth(SETTINGS["BEACON_SIZE"])
        painter.setPen(pen)
        painter.drawPoint(beacon.x, beacon.y)


def draw_beacon_indicators(painter: QPainter, map: map, robot: Robot):
    pen = QPen()
    pen.setStyle(Qt.DotLine)
    pen.setCapStyle(Qt.RoundCap)
    pen.setBrush(SETTINGS["COLOR_BEACON"])
    pen.setWidth(2)
    painter.setPen(pen)

    distances = [b.distance_to(robot.x, robot.y) for b in map.beacons]
    closest_beacon_id = distances.index(min(distances))

    for i, beacon in enumerate(map.beacons):
        if beacon.distance_to(robot.x, robot.y) <= SETTINGS["BEACON_INDICATOR_DISTANCE"]:
            painter.drawLine(beacon.x, beacon.y, robot.x, robot.y)
            if i == closest_beacon_id:
                pen.setWidth(1)
                pen.setStyle(Qt.SolidLine)
                painter.setPen(pen)
                painter.drawEllipse(QPoint(beacon.x, beacon.y), SETTINGS["BEACON_SIZE"] * 1.2,
                                    SETTINGS["BEACON_SIZE"] * 1.2)
                pen.setWidth(2)
                pen.setStyle(Qt.DotLine)
                painter.setPen(pen)


def draw_trace(painter: QPainter, trace: QPainterPath):
    pen = QPen()
    pen.setStyle(Qt.SolidLine)
    pen.setCapStyle(Qt.RoundCap)
    pen.setBrush(SETTINGS["COLOR_TRACE"])
    pen.setWidth(3)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)

    painter.drawPath(trace)


def draw_filter_trace(painter: QPainter, trace: QPainterPath):
    pen = QPen()
    pen.setStyle(Qt.DashLine)
    pen.setCapStyle(Qt.RoundCap)
    pen.setBrush(SETTINGS["COLOR_FILTER_TRACE"])
    pen.setWidth(3)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)

    painter.drawPath(trace)


def draw_filter_covariance_ellipse(painter: QPainter, x, y, cov_x, cov_y, heading):
    pen = QPen()
    pen.setStyle(Qt.SolidLine)
    pen.setBrush(SETTINGS["COLOR_FILTER_TRACE"])
    pen.setWidth(2)
    painter.setPen(pen)
    painter.setBrush(Qt.white)

    heading = math.degrees(heading)

    painter.translate(x, y)
    painter.rotate(heading)

    # scaling
    cov_x *= SETTINGS["COV_SCALING"]
    cov_y *= SETTINGS["COV_SCALING"]

    print(cov_y)
    print(cov_x)
    print()

    rect = QtCore.QRect(-cov_x / 2, - cov_y / 2, cov_x, cov_y)
    painter.drawEllipse(rect)

    painter.resetTransform()
