import face_recognition 
import numpy as np 
import os

database_path = '../images/database/'
test_path = '../images/test_img/'

test_img = [image for image in os.listdir(test_path)]
img_name = test_img[0]

original_img = face_recognition.load_image_file(os.path.join(database_path, img_name))
original_face_encoding = face_recognition.face_encodings(original_img)[0]

test_img = face_recognition.load_image_file(os.path.join(test_path, img_name))
test_face_location = face_recognition.face_locations(test_img)
test_img_encoding = face_recognition.face_encodings(test_img, test_face_location)

match = face_recognition.compare_faces(original_face_encoding, test_img_encoding)
print('match->', match)
