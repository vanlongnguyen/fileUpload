from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
import os
import sys

app = Flask(__name__)
api = Api(app)
UPLOAD_DIRECTORY = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_DIRECTORY
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'zip'}


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])

def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return filename + ' is uploaded successfully'
		else:
			message = ', ' .join(ALLOWED_EXTENSIONS)
			return 'Format is invalid to upload, only except: ' + message

@app.route("/files", methods = ['GET'])

def list_files():
	files = []
	for filename in os.listdir(UPLOAD_DIRECTORY):
		path = os.path.join(UPLOAD_DIRECTORY, filename)
		if os.path.isfile(path):
			abs_path = os.path.abspath(filename)
			files.append(abs_path)
	return jsonify(files)

if __name__ == '__main__':
	app.run(debug=True)
