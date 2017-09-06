from sklearn.externals import joblib
import json
import os

male_model = joblib.load("M.pkl")
female_model = joblib.load("F.pkl")

embeddings = json.loads(open("test.json").read())

for filename in os.listdir("test_images"):
    print(filename)
    embedding = embeddings[filename]
    print(male_model.predict([embedding]))
    print(female_model.predict([embedding]))