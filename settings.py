from PyQt5.QtGui import QColor

SETTINGS = {}

SETTINGS["DELTA_T"] = 0.01
SETTINGS["BEACON_INDICATOR_DISTANCE"] = 300
SETTINGS["TRACE_SMOOTHING"] = 100
SETTINGS["DISTANCE_BETWEEN_COV_CIRCLES"] = 100
SETTINGS["VERY_SMALL_NUMBER"] = 0.1e-10

# COLORS
SETTINGS["COLOR_ROBOT"] = QColor()
SETTINGS["COLOR_ROBOT"].setNamedColor("#005c86")

SETTINGS["COLOR_BEACON"] = QColor()
SETTINGS["COLOR_BEACON"].setNamedColor("#c34a36")

SETTINGS["COLOR_INDICATOR"] = SETTINGS["COLOR_BEACON"].lighter(400)

SETTINGS["COLOR_TRACE"] = QColor()
SETTINGS["COLOR_TRACE"].setNamedColor("#0088ac")

SETTINGS["COLOR_FILTER_TRACE"] = QColor()
SETTINGS["COLOR_FILTER_TRACE"].setNamedColor("#904579")

SETTINGS["COLOR_BACKGROUND"] = QColor()
SETTINGS["COLOR_BACKGROUND"].setNamedColor("#ede9d0")

# MAP
SETTINGS["MAP_WIDTH"] = 1600
SETTINGS["MAP_HEIGHT"] = 1000

SETTINGS["ROBOT_RADIUS"] = 30
SETTINGS["BEACON_SIZE"] = 8