from flask import Flask, render_template, request
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

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1,Firefox=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def upload_f():
	if os.path.exists(test_path):
		shutil.rmtree(test_path)
	if os.path.exists(disp_path):
		shutil.rmtree(disp_path)
	if not os.path.exists(test_path):
		os.mkdir(test_path)
	if not os.path.exists(disp_path):
		os.mkdir(disp_path)
	return render_template('upload.html', the_title="Face Recognition testing portal" )

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
		# return 'file uploaded successfully'

		test = [file for file in os.listdir(test_path)]
		img_name = test[0]
		print('img_name->', img_name)

		original_img = face_recognition.load_image_file(os.path.join(database_path, img_name))
		original_face_encoding = face_recognition.face_encodings(original_img)[0]

		test_img = face_recognition.load_image_file(os.path.join(test_path, img_name))
		test_face_location = face_recognition.face_locations(test_img)
		test_img_encoding = face_recognition.face_encodings(test_img, test_face_location)

		match = face_recognition.compare_faces(original_face_encoding, test_img_encoding)
		# print('match ->', type(match[0]))
		or_img = cv2.imread(os.path.join(database_path, img_name))
		or_img = cv2.resize(or_img, (300, 300))
		cv2.imwrite('./static/disp/original.jpg', or_img)

		t_img = cv2.imread(os.path.join(test_path, img_name))
		t_img = cv2.resize(t_img, (300, 300))
		cv2.imwrite('./static/disp/test.jpg', t_img)

		if match[0] == True:
			hists = os.listdir('static/disp/')
			hists = ['disp/' + file for file in hists]
			print(hists)
			return render_template('report.html', hists = hists, the_title="Photo matched")
		else:
			hists = os.listdir('static/disp/')
			hists = ['disp/' + file for file in hists]
			print(hists)
			return render_template('report.html', hists = hists, the_title="Photo not matched") 
		
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug = True)