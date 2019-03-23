import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

from settings import SETTINGS
from view.widgets import Environment, TrackingWidget


class App(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle('Kalman Localization')
        self.resize(SETTINGS["MAP_WIDTH"], SETTINGS["MAP_HEIGHT"])

        self.layout = QVBoxLayout(self)

        # WIDGETS
        self.environment_widget = Environment(self)
        self.tracking_widget = TrackingWidget(self.environment_widget.robot, parent=self)

        # ADD WIDGETS
        self.layout.addWidget(self.environment_widget)
        self.layout.addStretch(1)
        self.layout.addWidget(self.tracking_widget)
        self.environment_widget.setFocus(True)

        self.setLayout(self.layout)

    def step(self):
        self.environment_widget.animate()
        self.tracking_widget.update_indicators()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = App()
    main.show()

    timer = QTimer()
    timer.timeout.connect(main.step)
    timer.start(SETTINGS["DELTA_T"] * 100)

    app.exec_()
