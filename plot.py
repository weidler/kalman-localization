import ast
import re

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6

with open("results/experiment.txt", "r") as f:
    traces = f.readlines()

fig, axis_one = plt.subplots(1)
axis_two = axis_one.twinx()

corr_trace = ast.literal_eval(traces[1])
pred_trace = ast.literal_eval(traces[2])
gain_trace = ast.literal_eval(traces[3])

axis_one.plot(corr_trace, label="Correction Mean Squared Error")
axis_one.plot(pred_trace, label="Prediction Mean Squared Error")
axis_two.plot(gain_trace, label="Kalman Gain", color="tab:green")

plt.xlabel("Time Step")
axis_one.set_ylabel("Mean Squared Error")
axis_two.set_ylabel("Kalman Gain")

axis_one.set_title("Mean Squared Error")

plt.ylim(bottom=0)
plt.xlim(left=0)
axis_two.set_ylim(top=1)

axis_one.legend()

plt.show()