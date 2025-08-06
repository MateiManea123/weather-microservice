from flask import Flask, render_template, jsonify
from pymongo import MongoClient

from services.db_intialiser import init_database

app = Flask(__name__)
db = init_database()

@app.route("/")
def index():

    city_names = db.list_collection_names()
    return render_template("index.html", cities=city_names)

@app.route("/data/<city>")
def get_city_data(city):
    result = []
    collection = db[city]
    data = collection.find().sort("time_added", 1)
    for doc in data:
        result.append([
        {
            "timestamp": doc.get("time_added"),
            "temperature": doc.get("temperature")
        }
    ])
    print(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
