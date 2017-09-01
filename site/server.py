from flask import Flask, request
import json
import sqlite3

conn = sqlite3.connect('data.db')
db = conn.cursor()

app = Flask("ranker", static_url_path="")

@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route('/save', methods=["GET"])
def get_results():
  
    db.execute("INSERT INTO ranks VALUES ('" + request.args["filename"] + "', " + request.args["rank"] + ")")
    conn.commit()
      
    return "good"


app.run(host="0.0.0.0", port=80)