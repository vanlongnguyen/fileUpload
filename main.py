from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
from zipfile import ZipFile 
import os
import sys
import re
import shutil
from PIL import Image
import copy


app = Flask(__name__)
api = Api(app)
store_path = 'assests'
tmp_path = 'tmp/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'zip'}
ALLOWED_RENAMED = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower()


def rename_files():
	if not os.path.isdir(store_path):
		os.mkdir(store_path)
	for file in os.listdir(tmp_path):
		if allowed_file(file) in ALLOWED_RENAMED:
			new_store_path = tmp_path + '/'
			os.rename(tmp_path + file, store_path + '/' +  file.replace(' ', '_'))
	return 'renamed'

def clean_up():
	if os.path.isdir(tmp_path):
		shutil.rmtree(tmp_path)
		return 'cleaned tmp folder'

def do_generate_image(files, thumbnail_des, file, img_origin, extra_name, size):
	filename = file.rsplit('.', 1)[0].lower()
	filetype = file.rsplit('.', 1)[1].lower()

	img = copy.deepcopy(img_origin)

	img.thumbnail(size)
	thumb = thumbnail_des + '/' + filename + extra_name + '.' + filetype
	img.save(thumb, filetype)
	files.append(thumb)

# LIST UPLOADTED FILES
@app.route("/files", methods = ['GET'])
def list_files():
	clean_up()
	files = []
	for file in os.listdir(store_path):
		files.append(os.path.abspath(store_path + '/' + file))
	return jsonify(files)



# GENERAT THUMBNAILS
@app.route("/generate-thumbnails", methods = ['GET'])
def generate_thumbnail():
	size_32 = 32, 32
	size_64 = 64, 64
	origin = '_original'

	files = []

	thumbnail_des = os.path.abspath('thumbnails_generated')

	if not os.path.isdir(thumbnail_des):
		os.mkdir(thumbnail_des)
	for file in os.listdir(store_path):
		img_origin = Image.open(os.path.abspath(store_path+'/'+file))
		w, h = img_origin.size
		
		if w >= 128 and h >= 128:
			do_generate_image(files, thumbnail_des, file, img_origin, '_32' , size_32)

			do_generate_image(files, thumbnail_des, file, img_origin, '_64', size_64)
		else:
			do_generate_image(files, thumbnail_des, file, img_origin, origin , img_origin.size)

	return 'Generate thumbnails from original images successfully \n' + str(files)


# UPLOADER
@app.route('/uploader', methods = ['GET', 'POST'])

def upload_file():
	if request.method == 'POST':
		try:
			file = request.files['file']
			if not os.path.isdir(tmp_path):
				os.mkdir(tmp_path)
			if file and allowed_file(file.filename) in ALLOWED_EXTENSIONS:
				filename = secure_filename(file.filename)
				file.save(os.path.join(tmp_path, filename))
				path = os.path.join(tmp_path, filename)
				if os.path.isfile(path) and allowed_file(filename) == 'zip':
					with ZipFile(os.path.join(tmp_path, file.filename), 'r') as zip_ref:
						zip_ref.printdir()
						zip_ref.extractall(tmp_path)
				else:
					rename_files()
					return os.path.abspath(store_path + '/'+ filename)
				rename_files()
				return list_files()
			else:
				message = ', ' .join(ALLOWED_EXTENSIONS)
				return 'Format is invalid to upload, only except: ' + message
		except Exception as e:
			return str(e)


if __name__ == '__main__':
	app.run(debug=True)
