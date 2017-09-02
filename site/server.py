from flask import Flask, request
import json

app = Flask("ranker", static_url_path="")

@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route('/save', methods=["GET"])
def get_results():
    with open("data.json", "r+") as f:
        data = f.read()
        f.seek(0)

        data = json.loads(data)
        if not request.args["filename"] in data:
            data[request.args["filename"]] = []
        data[request.args["filename"]].append(int(request.args["rank"]))

        f.write(json.dumps(data))
        f.truncate()
    return "good"


