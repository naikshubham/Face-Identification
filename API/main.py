from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
import os 
import shutil
import face_recognition
import cv2
from dotenv import find_dotenv, load_dotenv
import asyncio

class Server():

	app = Flask(__name__)

	def __init__(self, database_path, test_path):
		self.database_path = database_path
		self.test_path = test_path
	
	# @app.after_request
	# def add_header(response):
	# 	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1,Firefox=1'
	# 	response.headers['Cache-Control'] = 'public, max-age=0'
	# 	return response

	@app.route('/api/facematch', methods = ['GET', 'POST'])
	def face_match(self):
		if os.path.exists(self.test_path):
			shutil.rmtree(self.test_path)
		if not os.path.exists(self.test_path):
			os.mkdir(self.test_path)

		if request.method == 'POST':
			f = request.files['file']
			f.save(os.path.join(self.test_path,secure_filename(f.filename)))

			test = [file for file in os.listdir(self.test_path)]
			img_name = test[0]
			print('img_name->', img_name)

			original_img = face_recognition.load_image_file(os.path.join(self.database_path, img_name))
			original_face_encoding = face_recognition.face_encodings(original_img)[0]

			test_img = face_recognition.load_image_file(os.path.join(self.test_path, img_name))
			test_face_location = face_recognition.face_locations(test_img)
			test_img_encoding = face_recognition.face_encodings(test_img, test_face_location)

			match = face_recognition.compare_faces(original_face_encoding, test_img_encoding)
			
			if match is True:
				response = {'match': True, 'status': 'OK'}
			else:
				response = {'match': False, 'status': 'OK'}
			
			return jsonify(response)
		
if __name__ == '__main__':
	load_dotenv(find_dotenv())
	database_path = os.environ.get("database_path")
	test_path = os.environ.get("test_path")
	host = os.environ.get("HOST")
	port = int(os.environ.get("PORT"))
	srv = Server(database_path,
				test_path)
	# srv.app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER")
	# srv.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
	srv.app.run(host, port, debug = True)