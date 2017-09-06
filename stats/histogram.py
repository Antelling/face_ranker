import json
import numpy as np
from matplotlib import pyplot as plt

with open("../site/data.json") as f:
    data = json.loads(f.read())

f, axarray = plt.subplots(1, 2, sharex=False, sharey=True)

for ax_fun in (axarray[0], np.median), (axarray[1], np.mean):
    scores = []

    for filename in data:
        good_nums = [n for n in data[filename] if 0 < n < 11]
        scores.append(ax_fun[1](good_nums))

    ax_fun[0].hist(scores, 9, edgecolor="black")
    ax_fun[0].set_xticks(range(1, 11))
    ax_fun[0].set_title(ax_fun[1].__name__)

plt.show()