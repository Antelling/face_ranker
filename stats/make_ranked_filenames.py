import os, json
import numpy as np
from shutil import copyfile, rmtree

with open("../site/data.json") as f:
    data = json.loads(f.read())

pairs = []

for filename in data:
    good_nums = [n for n in data[filename] if 0 < n < 11]
    pairs.append((
        filename,
        np.mean(good_nums)
    ))

pairs.sort(key=lambda t: t[1])

male_files = os.listdir("../site/static/M")
female_files = os.listdir("../site/static/F")

rmtree("ranked_filenames")
os.makedirs("ranked_filenames")

for i, face in enumerate(pairs):
    try:
        filename = ""
        if face[0] in male_files:
            filename = os.path.join("../site/static/M", face[0])
        elif face[0] in female_files:
            filename = os.path.join("../site/static/F", face[0])
        else:
            print("error")

        copyfile(filename, os.path.join("ranked_filenames", str(face[1]) + "-" + str(i) + ".png"))
    except:
        pass
