from PyQt5.QtGui import QColor

SETTINGS = {
    "DELTA_T": 0.01,
    "BEACON_INDICATOR_DISTANCE": 300,
    "TRACE_SMOOTHING": 1,

    # COLORS
    "COLOR_ROBOT": QColor(255, 0, 0),
    "COLOR_BEACON": QColor(0, 0, 255),
    "COLOR_INDICATOR": QColor(0, 0, 255).lighter(400),
    "COLOR_TRACE": QColor(0, 0, 0),
    "COLOR_BACKGROUND": QColor(255, 255, 255)
}
