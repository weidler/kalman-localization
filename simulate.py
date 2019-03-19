import sys
import time

from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsView, QGraphicsScene

from view.frame import DrawingFrame

DELTA_T = 0.01

if __name__ == "__main__":
    app = QApplication(sys.argv)
    drawing_panel = DrawingFrame()
    drawing_panel.simulate()

    app.exec_()
