import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene

from view.component import CircleRobot


class DrawingFrame(QGraphicsView):

    def __init__(self):
        super().__init__()
        self.resize(1000, 800)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.setWindowTitle("Kalman Localization")
        self.show()

    def simulate(self):
        pen = QtGui.QPen(QtGui.QColor(Qt.red))
        brush = QtGui.QBrush(pen.color().darker(255))
        robot = CircleRobot(100, 100, 20)
        self.scene.addItem(robot)
        for i in range(100):
            self.scene.clear()
            self.scene.addItem(robot)
            QtGui.QGuiApplication.processEvents()
            time.sleep(0.001)
