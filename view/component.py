import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication


class CircleRobot(QtWidgets.QGraphicsEllipseItem):

    def __init__(self, center_x, center_y, r):
        super(CircleRobot, self).__init__(center_x - r, center_y - r, r, r)
        self.r = r
        self.center_y = center_y
        self.center_x = center_x

    def paint(self, painter, option, widget=None):
        super(CircleRobot, self).paint(painter, option, widget)
        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.red)
        painter.drawEllipse(option.rect)

        painter.restore()
