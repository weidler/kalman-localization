import ast
import re

import matplotlib.pyplot as plt
from pylab import rcParams
rcParams['figure.figsize'] = 8, 6

with open("results/2019-03-25 13:47:47.678183.txt", "r") as f:
    traces = f.readlines()

fig, axs = plt.subplots(1)

mse_trace = ast.literal_eval(traces[1])

axs.plot(mse_trace, label="Correction Mean Squared Error")

plt.xlabel("Time Step")
plt.ylabel("Mean Squared Error")

axs.set_title("Mean Squared Error")

plt.ylim(bottom=0)
plt.xlim(left=0)

axs.legend()

plt.show()