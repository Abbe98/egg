import uuid
import os
from functools import wraps
from flask import Flask
from flask import request
from flask import abort
from flask import send_from_directory

app = Flask(__name__)
key = ''
storage = '/storage/'

@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.errorhandler(405)
def override_405(e):
    return '', 404

def require_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get('X-Api-Key') == key:
            return f(*args, **kwargs)
        abort(404)
    return decorated

def file_with_uuid_exists(uuid):
    for filename in os.listdir('.' + storage):
        if filename.startswith(str(uuid)):
            return filename
    return False

def valid_file_extension(extension):
    valid = ['jpeg', 'jpg', 'png', 'txt', 'html', 'csv', 'mp3', 'gif', 'mp4', 'json', 'xml', 'gpx', 'geojson', 'svg', 'dat', 'pdf', 'doc', 'docx', 'tar', 'zip']

    if extension in valid:
        return True

    return False

@app.route('/', methods=['POST'])
@require_key
def upload_file():
    if 'file' not in request.files:
        abort(404)

    upload = request.files['file']
    extension = os.path.splitext(upload.filename)[1][1:].lower()

    if not valid_file_extension(extension):
        abort(404)

    filename = str(uuid.uuid4()) + '.' + extension
    upload.save('.' + storage + filename)
    return filename

@app.route('/<uuid:id>', methods=['GET', 'DELETE'])
@require_key
def get(id):
    filename = file_with_uuid_exists(id)

    if not filename:
        abort(404)

    if request.method == 'GET':
        return send_from_directory(os.path.join(os.getcwd() + storage), str(filename))

    if request.method == 'DELETE':
        os.remove('.' + storage + filename)
        return '', 204

if __name__ == '__main__':
    app.run()
