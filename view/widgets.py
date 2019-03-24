import itertools

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainterPath, QPainter, QPen
from PyQt5.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect

from filters.kalman_filter import Kalman
from core.agent import Robot
from core.map import Map, Beacon
from settings import SETTINGS
from view.drawer import draw_beacon_indicators, draw_beacons, draw_trace, draw_filter_trace, \
    draw_filter_covariance_ellipse, draw_robot


class Environment(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.resize(SETTINGS["MAP_WIDTH"], SETTINGS["MAP_HEIGHT"])

        self.map = Map(SETTINGS["MAP_WIDTH"], SETTINGS["MAP_HEIGHT"])
        self.robot = Robot(SETTINGS["ROBOT_RADIUS"], self.map)
        self.filter = Kalman(self.robot)

        self.trace = QPainterPath()
        self.trace.moveTo(QPoint(self.robot.x, self.robot.y))
        self.estimated_trace = QPainterPath()
        self.estimated_trace.moveTo(QPoint(self.robot.x, self.robot.y))
        self.covariance_ellipses = []

        for x, y in itertools.product(range(200, SETTINGS["MAP_WIDTH"], 200), range(200, SETTINGS["MAP_HEIGHT"], 200)):
            self.map.add_beacon(Beacon(x, y))

        self.trace_smooth_level = SETTINGS["TRACE_SMOOTHING"]

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), SETTINGS["COLOR_BACKGROUND"])
        self.setPalette(p)

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
        prediction = self.filter.prediction()
        correction = self.filter.correction()

        estimation = correction

        # print(f"{self.robot.x - estimation[0,0]}\n{self.robot.y - estimation[1,0]}\n")

        # TRACES
        if self.trace_smooth_level == SETTINGS["TRACE_SMOOTHING"]:
            self.trace.lineTo(QPoint(self.robot.x, self.robot.y))
            self.estimated_trace.lineTo(QPoint(estimation[0, 0], estimation[1, 0]))
        elif self.trace_smooth_level == 0:
            self.trace_smooth_level = SETTINGS["TRACE_SMOOTHING"]
        else:
            self.trace_smooth_level -= 1

        # COVARIANCE CIRCLES
        if self.trace.length() - (len(self.covariance_ellipses) * SETTINGS["DISTANCE_BETWEEN_COV_CIRCLES"]) >= SETTINGS[
            "DISTANCE_BETWEEN_COV_CIRCLES"]:
            self.covariance_ellipses.append((self.filter.mu[0], self.filter.mu[1], self.filter.sigma[0, 0], self.filter.sigma[1, 1], self.filter.mu[2]))

        self.update()


class TrackingWidget(QWidget):

    def __init__(self, robot, parent: QWidget = None):
        super().__init__(parent)

        self.robot = robot

        hcenter = parent.width() * 0.5
        self.tracker_width = parent.width() * 0.5
        self.tracker_height = 60
        self.setGeometry(hcenter - 0.5 * self.tracker_width, 30, self.tracker_width, self.tracker_height)

        # VELOCITY
        self.indicators = QLabel(self)
        self.indicators.setText(f"Velocity: {self.robot.v}\nRotation Velocity: {self.robot.w}")
        self.indicators.setAlignment(QtCore.Qt.AlignCenter)
        self.indicators.setGeometry(0, 0, self.tracker_width, self.tracker_height)
        text_opacity = QGraphicsOpacityEffect(self)
        self.indicators.setGraphicsEffect(text_opacity)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        pen = QPen()
        pen.setStyle(Qt.SolidLine)
        pen.setBrush(SETTINGS["COLOR_BACKGROUND"].darker(200))
        pen.setWidth(6)

        qp.setOpacity(0.6)
        qp.setPen(pen)
        qp.setBrush(SETTINGS["COLOR_BACKGROUND"].darker(120))
        qp.drawRect(0, 0, self.tracker_width, self.tracker_height)
        qp.end()

    def update_indicators(self):
        self.indicators.setText(f"Velocity: {round(self.robot.v, 1)}\nRotation Velocity: {round(self.robot.w, 1)}")
