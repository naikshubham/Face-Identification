from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
import os 
import shutil
import face_recognition
import cv2

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './images/test/'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

database_path = './images/database/'
test_path = './images/test/'
disp_path = './static/disp/'

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if os.path.exists(test_path):
		shutil.rmtree(test_path)
	if not os.path.exists(test_path):
		os.mkdir(test_path)

	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(test_path,secure_filename(f.filename)))

		test = [file for file in os.listdir(test_path)]
		img_name = test[0]
		print('img_name->', img_name)

		original_img = face_recognition.load_image_file(os.path.join(database_path, img_name))
		original_face_encoding = face_recognition.face_encodings(original_img)[0]

		test_img = face_recognition.load_image_file(os.path.join(test_path, img_name))
		test_face_location = face_recognition.face_locations(test_img)
		test_img_encoding = face_recognition.face_encodings(test_img, test_face_location)

		match = face_recognition.compare_faces(original_face_encoding, test_img_encoding)
		
		if match is True:
			response = {'match': True, 'status': 'OK'}
		else:
			response = {'match': False, 'status': 'OK'}
		
		return jsonify(response)
		
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug = True)	