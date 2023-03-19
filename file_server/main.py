from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/images/<filename>')
def get_image(filename):
    print(filename)
    return send_from_directory("../images", filename)

@app.errorhandler(404)
def page_not_found(e):
    return send_from_directory("../images", "xdd.png")

if __name__ == "__main__":
    app.run(debug=True)