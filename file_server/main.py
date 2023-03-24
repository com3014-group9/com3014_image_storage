from flask import Flask, send_from_directory, send_file, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import pprint
import os
import time

UPLOAD_FOLDER = '../images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def build_url_from_path(filepath):
    return "/images/" + filepath.split('\\')[-1]

@app.route('/images/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            id = image_db.image_data.find_one(sort=[("id", -1)])
            id = id["id"] + 1 if id != None else 0

            tags = request.form['tags'].split(" ")
            print(tags)

            image_db.image_data.insert_one({"path" : filepath, "id" : id, "owner" : request.form['owner'], "tags" : tags, "timestamp" : int(time.time())})

            file.save(filepath)

            return send_from_directory("../images", filename)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory("../images", filename)

@app.route('/images/id/<id>')
def get_image_by_id(id):
    image = image_db.image_data.find_one({"id" : int(id)})

    if image == None:
        return send_from_directory("../images", "xdd.png")
    return send_file("..\\" + image["path"])

@app.route('/images/user/latest/<owner>')
def get_last_user_image(owner):
    image = image_db.image_data.find_one({"owner" : owner}, sort=[("timestamp", -1)])

    if image == None:
        return send_from_directory("../images", "xdd.png")

    return send_file("..\\" + image["path"])

@app.route('/images/user/<owner>')
def get_user_images(owner):
    start = int(request.args.get('from'))
    stop = int(request.args.get('to'))

    cur = image_db.image_data.find({"owner" : owner}, sort=[("timestamp", -1)]).skip(start).limit(stop-start)

    images = []
    for doc in cur:
        images.append(build_url_from_path(doc["path"]))

    return jsonify(images)

@app.route('/images/tag/<tag>')
def get_images_by_tag(tag):
    start = int(request.args.get('from'))
    stop = int(request.args.get('to'))

    cur = image_db.image_data.find({"tags" : {"$in" : [tag]}}, sort=[("timestamp", -1)]).skip(start).limit(stop-start)

    images = []
    for doc in cur:
        images.append(build_url_from_path(doc["path"]))

    return jsonify(images)

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory("../images", "xdd.png")

if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    image_db = client.com3014_images
    app.run(debug=True)