from sklearn.externals import joblib
import json
import os
try:
    from .compare import TripletEmbedding
except:
    from compare import TripletEmbedding


te = TripletEmbedding()

male_model = joblib.load("M.pkl")
female_model = joblib.load("F.pkl")


for filename in os.listdir("test_images"):
    try:
        embedding = json.loads(open(os.path.join("test_embeddings", filename.replace(".jpg", ".json"))).read())
    except Exception as e:
        print("generating embedding for " + filename)
        embedding = te.getEmbedding(os.path.join("test_images", filename))
        with open(os.path.join("test_embeddings", filename.replace(".jpg", ".json")), "w") as f:
            f.write(json.dumps(embedding.tolist()))

    prediction = male_model.predict([embedding]) if filename[0] == "m" else female_model.predict([embedding])
    print(filename + " - " + str(prediction[0]))