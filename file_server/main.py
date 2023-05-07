from flask import Flask, send_from_directory, send_file, request, redirect, url_for, jsonify, Blueprint, current_app, g
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import pprint
import os
import time
import requests

from auth_middleware import auth_required

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

imager = Blueprint('imager', __name__, url_prefix='/images')

def create_app():
    app = Flask(__name__)
    app.register_blueprint(imager)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.teardown_appcontext_funcs.append(close_db)

    return app

# Connect to a mongo database and get the images collections
def get_db_client():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")

    return client

# Connect to DB and store in context
def get_db():
    if 'db' not in g:
        g.db = get_db_client()
    
    return g.db.com3014_images  

# Disconnect from DB if we are connected
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# Check if the file is allowed (i.e., it has an image extension)
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# The helper function for taking a path and returning a URL to an image
# this is useful for queries that return multiple images at once
def build_url_from_path(filepath):
    return  "/" + filepath.split('\\')[-1]

# Upload image to the backend and save a path to it to the database
@imager.route('/upload', methods=['POST'])
@auth_required
def upload_file(user_id):
    if 'file' not in request.files:
         return {"error" : "Missing image"}, 400

    file = request.files['file']
    
    if file.filename == '':
        return {"error" : "Empty filename"}, 400

    if "owner" not in request.form or "tags" not in request.form:
        return {"error" : "Missing fields"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        id = get_db().image_data.find_one(sort=[("id", -1)])
        id = id["id"] + 1 if id != None else 0

        #tags = request.form['tags'].split(" ")

         # Call the other microservice and get a string value returned
        files = {'file': file.read()}
        #Replace the following link with whatever it gets assigned to by the docker (it should be local host by default or the app's name)
        response = requests.post('http://localhost:3303/get_tags', files=files)
        tags = response.text.strip()

        get_db().image_data.insert_one({"path" : filepath, "id" : id, "owner" : request.form['owner'], "tags" : tags, "timestamp" : int(time.time())})
        
        file.save(filepath)

        return {"file": filename}, 201
    else:
        return {"error": "Invalid file type"}, 400

# Get image using its filename
@imager.route('/<filename>', methods=['GET'])
@auth_required
def get_image(user_id, filename):
    if os.path.isfile(f"images/{filename}"):
        return send_from_directory("images", filename), 200
    else:
        return send_from_directory("images", "xdd.png"), 404

# Get image using its id
@imager.route('/id/<id>', methods=['GET'])
@auth_required
def get_image_by_id(user_id, id):
    image = get_db().image_data.find_one({"id" : int(id)})
    cur = get_db().image_data.find({})
    print(len(list(cur)))
    for each in cur:
        print(each)
    if image == None:
        return send_from_directory("images", "xdd.png"), 404
    return send_file(image["path"]), 200

# Get last image posted by the user
@imager.route('/user/latest/<owner>', methods=['GET'])
@auth_required
def get_last_user_image(user_id, owner):
    image = get_db().image_data.find_one({"owner" : owner}, sort=[("timestamp", -1)])

    if image == None:
        return send_from_directory("images", "xdd.png")

    return send_file(image["path"])

# Get all images posted by the user
@imager.route('/user/<owner>', methods=['GET'])
@auth_required
def get_user_images(user_id, owner):
    if 'from' not in request.args:
        start = 0
    else:
        start = int(request.args.get('from'))
    
    if 'to' not in request.args:
        stop = 50
    else:
        stop = int(request.args.get('to'))

    cur = get_db().image_data.find({"owner" : owner}, sort=[("timestamp", -1)]).skip(start).limit(stop-start)
    meow = list(cur)

    if len(meow) > 0:
        images = []
        for doc in meow:
            images.append(build_url_from_path(doc["path"]))
        return {'images' : images}, 200
    else:
        return send_from_directory("images", "xdd.png"), 404

# Get all images posted under the specified tag
@imager.route('/tag/<tag>', methods=['GET'])
@auth_required
def get_images_by_tag(user_id, tag):
    if 'from' not in request.args:
        start = 0
    else:
        start = int(request.args.get('from'))
    
    if 'to' not in request.args:
        stop = 50
    else:
        stop = int(request.args.get('to'))

    cur = get_db().image_data.find({"tags" : {"$in" : [tag]}}, sort=[("timestamp", -1)]).skip(start).limit(stop-start)
    meow = list(cur)
    
    if len(meow) > 0:
        images = []
        for doc in meow:
            images.append(build_url_from_path(doc["path"]))
        return {'images' : images}, 200
    else:
        return send_from_directory("images", "xdd.png"), 404

# Instead of default 404 page, send the xdd image to a user
@imager.errorhandler(404)
def page_not_found(e):
    return send_from_directory("images", "xdd.png")

if __name__ == "__main__":
    image_db = get_db_client().com3014_images
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5050)