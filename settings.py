from PyQt5.QtGui import QColor

SETTINGS = {"DELTA_T": 0.05,
            "BEACON_INDICATOR_DISTANCE": 200,
            "TRACE_SMOOTHING": 100,
            "DISTANCE_BETWEEN_COV_CIRCLES": 200,

            "INITIAL_COVARIANCE": 0.001,

            "MOTION_NOISE": 5,
            "MOTION_THETA_NOISE": 0.001,
            "MOTION_NOISE_ESTIMATION": 0.01,

            "SENSOR_NOISE": 25,
            "SENSOR_NOISE_ESTIMATION": 0.2,

            "COV_SCALING": 2000,

            "COLOR_ROBOT": QColor(),
            "COLOR_BEACON": QColor(),
            "COLOR_TRACE": QColor(),
            "COLOR_FILTER_TRACE": QColor(),
            "COLOR_BACKGROUND": QColor(),

            "MAP_WIDTH": 1600,
            "MAP_HEIGHT": 1000,
            "MAP_START": (400, 500),

            "ROBOT_RADIUS": 30,

            "EXPERIMENT_MODE": False,
            "ROBOT_START_V": 200,
            "ROBOT_START_W": -0.5,
            "EXPERIMENT_LENGTH": 252,  # steps until full circle

            "BEACON_SIZE": 8
            }

# COLORS
SETTINGS["COLOR_BACKGROUND"].setNamedColor("#ede9d0")
SETTINGS["COLOR_FILTER_TRACE"].setNamedColor("#904579")
SETTINGS["COLOR_TRACE"].setNamedColor("#0088ac")
SETTINGS["COLOR_INDICATOR"] = SETTINGS["COLOR_BEACON"].lighter(400)
SETTINGS["COLOR_BEACON"].setNamedColor("#c34a36")
SETTINGS["COLOR_ROBOT"].setNamedColor("#005c86")

#### SETS OF SETTINGS ####
DEMO_SETTINGS = {"DELTA_T": 0.1,
                 "BEACON_INDICATOR_DISTANCE": 300,
                 "TRACE_SMOOTHING": 1,
                 "DISTANCE_BETWEEN_COV_CIRCLES": 200,

                 "INITIAL_COVARIANCE": 0.000001,

                 "MOTION_NOISE": 0.01,
                 "MOTION_NOISE_ESTIMATION": 0.00001,

                 "SENSOR_NOISE": 0.004,
                 "SENSOR_NOISE_ESTIMATION": 0.9,

                 "COV_SCALING": 5000,

                 "COLOR_ROBOT": QColor(),
                 "COLOR_BEACON": QColor(),
                 "COLOR_TRACE": QColor(),
                 "COLOR_FILTER_TRACE": QColor(),
                 "COLOR_BACKGROUND": QColor(),

                 "MAP_WIDTH": 1600,
                 "MAP_HEIGHT": 1000,
                 "MAP_START": (400, 500),

                 "ROBOT_RADIUS": 30,

                 "EXPERIMENT_MODE": False,
                 "ROBOT_START_V": 200,
                 "ROBOT_START_W": -0.5,
                 "EXPERIMENT_LENGTH": 200,

                 "BEACON_SIZE": 8
}

SETTINGS = SETTINGS