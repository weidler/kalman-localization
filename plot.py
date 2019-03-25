import ast
import re

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6

with open("results/experiment.txt", "r") as f:
    traces = f.readlines()

fig, axs = plt.subplots(1)

corr_trace = ast.literal_eval(traces[1])
pred_trace = ast.literal_eval(traces[2])

axs.plot(corr_trace, label="Correction Mean Squared Error")
axs.plot(pred_trace, label="Prediction Mean Squared Error")

plt.xlabel("Time Step")
plt.ylabel("Mean Squared Error")

axs.set_title("Mean Squared Error")

plt.ylim(bottom=0)
plt.xlim(left=0)

axs.legend()

plt.show()