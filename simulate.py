import itertools
import math
import sys
import time

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPoint, Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene, QMainWindow

from core.agent import Robot
from core.map import Map, Beacon
from view.frame import DrawingFrame

DELTA_T = 0.01
BEACON_INDICATOR_DISTANCE = 300


def draw_robot(painter: QPainter, robot: Robot):
    robot_nose_x = int(robot.x + (robot.radius * math.cos(robot.theta)))
    robot_nose_y = int(robot.y + (robot.radius * math.sin(robot.theta)))

    pen = QPen()
    pen.setStyle(Qt.DashLine)
    pen.setBrush(Qt.black)
    pen.setWidth(3)

    painter.setPen(pen)
    painter.setBrush(Qt.green)

    painter.drawEllipse(QPoint(robot.x, robot.y), robot.radius, robot.radius)
    pen.setStyle(Qt.SolidLine)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)
    painter.drawLine(robot.x, robot.y, robot_nose_x, robot_nose_y)


def draw_beacons(painter: QPainter, map: Map):
    pen = QPen()
    pen.setBrush(Qt.red)
    pen.setWidth(6)
    pen.setCapStyle(Qt.RoundCap)
    painter.setPen(pen)

    for beacon in map.beacons:
        painter.drawPoint(beacon.x, beacon.y)


def draw_beacon_indicators(painter: QPainter, map: map, robot: Robot):
    pen = QPen()
    pen.setStyle(Qt.SolidLine)
    pen.setBrush(Qt.blue)
    pen.setWidth(2)
    painter.setPen(pen)

    for beacon in map.beacons:
        if beacon.distance_to(robot.x, robot.y) <= BEACON_INDICATOR_DISTANCE:
            painter.drawLine(beacon.x, beacon.y, robot.x, robot.y)


class App(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('Kalman Localization')
        self.resize(800, 800)

        self.robot = Robot(20, 100, 100)
        self.map = Map()

        for x, y in itertools.product(range(200, 601, 200), range(200, 601, 200)):
            self.map.add_beacon(Beacon(x, y))

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        draw_beacon_indicators(qp, self.map, self.robot)
        draw_robot(qp, self.robot)
        draw_beacons(qp, self.map)
        qp.end()

    def keyPressEvent(self, e):
        # INCREMENT v
        if e.key() == QtCore.Qt.Key_W:
            self.robot.increment_v()
        # INCREMENT w
        if e.key() == QtCore.Qt.Key_D:
            self.robot.increment_w()

        # DECREMENT v
        if e.key() == QtCore.Qt.Key_S:
            self.robot.decrement_v()
        # DECREMENT w
        if e.key() == QtCore.Qt.Key_A:
            self.robot.decrement_w()

        # STOP
        if e.key() == QtCore.Qt.Key_X:
            self.robot.stop()

        # STOP
        if e.key() == QtCore.Qt.Key_Escape:
            exit()

    def animate(self):
        self.robot.velocity_based_model()
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = App()
    main.show()

    timer = QTimer()
    timer.timeout.connect(main.animate)
    timer.start(33)

    app.exec_()
