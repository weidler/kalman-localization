import ast
import re

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6

fig, axis_one = plt.subplots(1)

noise = [200, 400, 1000]
corr_trace = [121.91, 62.49, 35.72]
pred_trace = [123.47, 65.54, 41.61]

axis_one.plot(noise, corr_trace, label="Correction MSE")
axis_one.plot(noise, pred_trace, label="Prediction MSE")

plt.xlabel("Sensor Range")
axis_one.set_ylabel("Average MSE")

axis_one.set_title("Influence of Sensor Range on Estimation MSE")

plt.ylim(bottom=0)
plt.xlim(left=200)

axis_one.legend()

plt.show()