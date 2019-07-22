from __future__ import division

import json
import random

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.svm import SVR
from sklearn.linear_model import HuberRegressor

from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from sklearn.decomposition import PCA

from sklearn.externals import joblib

import numpy as np

labels = json.loads(open("../site/data.json").read())

pipeline = Pipeline([
    ("decomp", PCA()),
    ("regressor", GradientBoostingRegressor())
])

param_grid = {
    "decomp__n_components": [96, 70, 50, 30],
    "regressor": [SVR(C=2.5), GradientBoostingRegressor(), HuberRegressor(), RandomForestRegressor()]
}


def flatten_dimension(d):
    n = len(d)
    step = 10 / n
    numbers = np.arange(0, 100, step)

    # okay so we want to snap our d to numbers
    # but we need to remember our original position
    # and we need to fuzz the numbers to avoid bad correlations
    structured_d = []
    for i, value in enumerate(d):
        structured_d.append({"index": i, "value": value + random.uniform(-.1, .1)})

    structured_d.sort(key=lambda x: x["value"])

    for i, value in enumerate(structured_d):
        structured_d[i]["flattened_value"] = numbers[i]

    structured_d.sort(key=lambda x: x["index"])

    d = []
    for value in structured_d:
        d.append(value["flattened_value"])
    return d

def score(estimator, new_X, new_y):
    estimator.fit(new_X, new_y)
    predictions = estimator.predict(X)
    error = np.mean(np.abs((predictions - y)))
    return -error


cv = GridSearchCV(pipeline, param_grid=param_grid, scoring=score)

for gender in "M", "F":
    embeddings = json.loads(open(gender + ".json").read())

    print("amount of embedded images: " + str(len(list(embeddings))))
    print("amount of labeled images: " + str(len(list(labels))))

    X = []
    y = []

    for filename in embeddings:
        if filename in labels:
            scores = labels[filename]
            l = [l for l in scores if 0 < l < 11]
            if len(l) > 0:
                l = np.mean(l)
                y.append(l)
                X.append(embeddings[filename])

    y = flatten_dimension(y)

    cv.fit(X, y)

    print(cv.best_score_ * -1)
    print(cv.best_params_)

    joblib.dump(cv.best_estimator_, gender + ".pkl")
