from flask import Flask, send_from_directory, send_file
from pymongo import MongoClient
import pprint

app = Flask(__name__)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory("../images", filename)

@app.route('/images/id/<id>')
def get_image_by_id(id):
    image = image_db.image_data.find_one({"id" : int(id)})

    if image == None:
        return send_from_directory("../images", "xdd.png")
    return send_file("..\\" + image["path"])

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory("../images", "xdd.png")

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    image_db = client.com3014_images
    app.run(debug=True)