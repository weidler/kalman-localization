import ast
import re

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6

fig, axis_one = plt.subplots(1)

motion_trace = ast.literal_eval([12.264565112922117, 13.702210715316683, 26.262139981300898, 94.59390023276706])
sensor_trace = ast.literal_eval(zzzz)

axis_one.plot(motion_trace, label="Motion Noise")
axis_one.plot(sensor_trace, label="Sensor Noise")

plt.xlabel("Noise Variance")
axis_one.set_ylabel("Average MSE")

axis_one.set_title("")

plt.ylim(bottom=0)
plt.xlim(left=0)

axis_one.legend()

plt.show()