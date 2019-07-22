import json, os
import numpy as np
from matplotlib import pyplot as plt

with open("../site/data.json") as f:
    data = json.loads(f.read())

men = os.listdir("../site/static/M")
women = os.listdir("../site/static/F")

f, axarray = plt.subplots(2, 2, sharex=False, sharey=True)
print(axarray)

for max_wax_fun in ([axarray[0][0], axarray[1][0]], np.median), ([axarray[0][1], axarray[1][1]], np.mean):
    men_scores = []
    women_scores = []

    for filename in data:
        good_nums = [n for n in data[filename] if 0 < n < 11]
        score = max_wax_fun[1](good_nums)
        if filename in men:
            men_scores.append(score)
        elif filename in women:
            women_scores.append(score)
        else:
            print(filename)


    max_wax_fun[0][0].hist(men_scores, 9, edgecolor="black")
    max_wax_fun[0][0].set_xticks(range(1, 11))
    max_wax_fun[0][0].set_title("men " + max_wax_fun[1].__name__)

    max_wax_fun[0][1].hist(women_scores, 9, edgecolor="black")
    max_wax_fun[0][1].set_xticks(range(1, 11))
    max_wax_fun[0][1].set_title("women " + max_wax_fun[1].__name__)

plt.show()