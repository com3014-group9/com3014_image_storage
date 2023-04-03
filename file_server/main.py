from flask import Flask, send_from_directory, send_file, request, redirect, url_for, jsonify, Blueprint, current_app, g
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import pprint
import os
import time

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

imager = Blueprint('imager', __name__, url_prefix='/images')

def create_app():
    app = Flask(__name__)
    app.register_blueprint(imager)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app

# Connect to a mongo database and get the images collections
def get_db_client():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")

    return client

def get_db():
    if 'db' not in g:
        g.db = get_db_client()
    
    return g.db.com3014_images  


# Check if the file is allowed (i.e., it has an image extension)
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# The helper function for taking a path and returning a URL to an image
# this is useful for queries that return multiple images at once
def build_url_from_path(filepath):
    return "/images/" + filepath.split('\\')[-1]

# Upload image to the backend and save a path to it to the database
@imager.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        id = get_db().image_data.find_one(sort=[("id", -1)])
        id = id["id"] + 1 if id != None else 0

        tags = request.form['tags'].split(" ")

        get_db().image_data.insert_one({"path" : filepath, "id" : id, "owner" : request.form['owner'], "tags" : tags, "timestamp" : int(time.time())})
        
        file.save(filepath)

        return {"file": filename}, 201
    else:
        return {"error": "Invalid file type"}, 404

# Get image using its filename
@imager.route('/<filename>', methods=['GET'])
def get_image(filename):
    if os.path.isfile(f"images/{filename}"):
        return send_from_directory("images", filename)
    else:
        return send_from_directory("images", "xdd.png")

# Get image using its id
@imager.route('/id/<id>', methods=['GET'])
def get_image_by_id(id):
    image = get_db().image_data.find_one({"id" : int(id)})

    if image == None:
        return send_from_directory("images", "xdd.png")
    return send_file(image["path"])

# Get last image posted by the user
@imager.route('/user/latest/<owner>', methods=['GET'])
def get_last_user_image(owner):
    image = get_db().image_data.find_one({"owner" : owner}, sort=[("timestamp", -1)])

    if image == None:
        return send_from_directory("images", "xdd.png")

    return send_file(image["path"])

# Get all images posted by the user
@imager.route('/user/<owner>', methods=['GET'])
def get_user_images(owner):
    start = int(request.args.get('from'))
    stop = int(request.args.get('to'))

    cur = get_db().image_data.find({"owner" : owner}, sort=[("timestamp", -1)]).skip(start).limit(stop-start)

    if len(list(cur)) > 0:
        images = []
        for doc in cur:
            images.append(build_url_from_path(doc["path"]))

        return jsonify(images)
    else:
        return send_from_directory("images", "xdd.png")

# Get all images posted under the specified tag
@imager.route('/tag/<tag>', methods=['GET'])
def get_images_by_tag(tag):
    start = int(request.args.get('from'))
    stop = int(request.args.get('to'))

    cur = get_db().image_data.find({"tags" : {"$in" : [tag]}}, sort=[("timestamp", -1)]).skip(start).limit(stop-start)

    if len(list(cur)) > 0:
        images = []
        for doc in cur:
            images.append(build_url_from_path(doc["path"]))

        return jsonify(images)
    else:
        return send_from_directory("images", "xdd.png")

# Instead of default 404 page, send the xdd image to a user
@imager.errorhandler(404)
def page_not_found(e):
    return send_from_directory("images", "xdd.png")

if __name__ == "__main__":
    image_db = get_db_client().com3014_images
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)