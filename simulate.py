import itertools
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QApplication, QMainWindow

from Pose_tracking.kalman_filter import Kalman
from core.agent import Robot
from core.map import Map, Beacon
from settings import SETTINGS
from view.drawer import draw_beacon_indicators, draw_beacons, draw_trace, draw_robot, draw_filter_trace, \
    draw_filter_covariance_ellipse


class App(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('Kalman Localization')
        self.resize(SETTINGS["MAP_WIDTH"], SETTINGS["MAP_HEIGHT"])

        self.map = Map(SETTINGS["MAP_WIDTH"], SETTINGS["MAP_HEIGHT"])
        self.robot = Robot(SETTINGS["ROBOT_RADIUS"], self.map, 100, 100)
        # self.filter = Kalman(self.robot.v, self.robot.w)

        self.trace = QPainterPath()
        self.trace.moveTo(QPoint(self.robot.x, self.robot.y))
        self.estimated_trace = QPainterPath()
        self.estimated_trace.moveTo(QPoint(self.robot.x, self.robot.y))
        self.covariance_ellipses = []

        for x, y in itertools.product(range(200, SETTINGS["MAP_WIDTH"], 200), range(200, SETTINGS["MAP_HEIGHT"], 200)):
            self.map.add_beacon(Beacon(x, y))

        self.trace_smooth_level = SETTINGS["TRACE_SMOOTHING"]
        self.steps_since_cov_circle = 0

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        draw_beacon_indicators(qp, self.map, self.robot)
        draw_beacons(qp, self.robot)
        draw_trace(qp, self.trace)
        draw_filter_trace(qp, self.estimated_trace)
        for ell in self.covariance_ellipses:
            draw_filter_covariance_ellipse(qp, *ell)


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
        # self.filter.prediction(self.robot)
        # self.filter.correction(self.robot)

        # TRACES
        if self.trace_smooth_level == SETTINGS["TRACE_SMOOTHING"]:
            self.trace.lineTo(QPoint(self.robot.x, self.robot.y))
            # self.estimated_trace.lineTo(QPoint(self.filter.mü_t[0], self.filter.mü_t[1]))
        elif self.trace_smooth_level == 0:
            self.trace_smooth_level = SETTINGS["TRACE_SMOOTHING"]
        else:
            self.trace_smooth_level -= 1

        self.steps_since_cov_circle += 1
        if self.steps_since_cov_circle >= SETTINGS["STEPS_BETWEEN_COV_CIRCLE"]:
            self.steps_since_cov_circle = 0
            self.covariance_ellipses.append((self.robot.x, self.robot.y, 30, 10, self.robot.theta))

        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = App()
    main.show()

    timer = QTimer()
    timer.timeout.connect(main.animate)
    timer.start(SETTINGS["DELTA_T"] * 1000)

    app.exec_()
