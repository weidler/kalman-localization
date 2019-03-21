import itertools
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow

from core.agent import Robot
from core.map import Map, Beacon
from settings import SETTINGS
from view.drawer import draw_beacon_indicators, draw_beacons, draw_trace, draw_robot


class App(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('Kalman Localization')
        self.resize(800, 800)

        self.robot = Robot(20, 100, 100)
        self.map = Map()
        self.trace = QPainterPath()
        self.trace.moveTo(QPoint(self.robot.x, self.robot.y))
        self.trace_smooth_level = SETTINGS["TRACE_SMOOTHING"]

        for x, y in itertools.product(range(200, 601, 200), range(200, 601, 200)):
            self.map.add_beacon(Beacon(x, y))

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        draw_beacon_indicators(qp, self.map, self.robot)
        draw_beacons(qp, self.map)
        draw_trace(qp, self.trace)
        draw_robot(qp, self.robot)
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

        if self.trace_smooth_level == SETTINGS["TRACE_SMOOTHING"]:
            self.trace.lineTo(QPoint(self.robot.x, self.robot.y))
        elif self.trace_smooth_level == 0:
            self.trace_smooth_level = SETTINGS["TRACE_SMOOTHING"]
        else:
            self.trace_smooth_level -= 1

        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = App()
    main.show()

    timer = QTimer()
    timer.timeout.connect(main.animate)
    timer.start(SETTINGS["DELTA_T"] * 1000)

    app.exec_()
