import face_recognition 
import numpy as np 
import os
import cv2

database_path = '../images/database/'
test_path = '../images/test_img/'

test_img = [image for image in os.listdir(test_path)]

for image in test_img:
	print('---'+image+'---')
	img_name = image.split('_')[0]
	try:
		original_img = face_recognition.load_image_file(os.path.join(database_path, img_name+'.jpg'))
	except:
		original_img = face_recognition.load_image_file(os.path.join(database_path, img_name+'.jpeg'))
	original_face_encoding = face_recognition.face_encodings(original_img)[0]

	test_img = face_recognition.load_image_file(os.path.join(test_path, image))
	test_face_location = face_recognition.face_locations(test_img)
	# print(test_face_location)
	# y1, y2,x1, x2 = test_face_location[0]
	# crop_img = test_img[y1:y2, x1:x2]
	test_img_encoding = face_recognition.face_encodings(test_img, test_face_location)

	org_img = cv2.imread(os.path.join(database_path, img_name+'.jpg'))
	if org_img is None:
		org_img = cv2.imread(os.path.join(database_path, img_name+'.jpeg'))
	test_img = cv2.imread(os.path.join(test_path, image))
	print(org_img.shape)
	org_img = cv2.resize(org_img, (500, 500))
	t_img = cv2.resize(test_img, (500, 500))
	f_img = np.hstack((org_img, t_img))

	match = face_recognition.compare_faces(original_face_encoding, test_img_encoding)
	print('match->', match)
	if match[0]:
		cv2.putText(f_img, 'matched', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), lineType=cv2.LINE_AA)
		cv2.imwrite('../images/matched/m_'+image, f_img)
	else:
		cv2.putText(f_img, 'not-matched', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), lineType=cv2.LINE_AA)
		cv2.imwrite('../images/unmatched/um_'+image, f_img)

# (170, 384, 491, 63) (547, 589, 932, 204)