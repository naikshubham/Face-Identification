from __future__ import print_function
import requests
import json
from flask import request
import cv2
from http.client import HTTPSConnection
from base64 import b64encode

GET_API_ENDPOINT = 'http://devdonation.jnms.org:10041/api/Processor/GetMismatchedAttendance'
POST_API_ENDPOINT = 'http://devdonation.jnms.org:10041'
post_url = POST_API_ENDPOINT +'/api/Processor/PostAttendanceResults'

c = 0 
content_type = 'application/json'
headers = {'content-type':content_type}

for i in range(2000):
    response = requests.get(GET_API_ENDPOINT, auth=('LMSAppUser', 'LMSAppUserPwd'))
    # print(json.loads(response.text))
    # print(response.headers)

    f_response = json.loads(response.text)
    with open('./jsons/data_'+str(c)+'.json', 'w') as f:
        json.dump(f_response, f)
    c += 1

    for data in f_response['CONTENT']:
        with open('urls.txt', 'a') as f:
            print(data['AttendanceId'], data['EmployeeId'], data['AttendanceSelfieUrl'], file=f)
    
    result = {"CONTENT":[]}

    for d in f_response['CONTENT']:
        result['CONTENT'].append({'AttendanceId':d['AttendanceId'], 'Result':'true'})
    # print(result)
    response = requests.post(post_url, data=data, headers=headers, auth=('LMSAppUser', 'LMSAppUserPwd'))
    print(json.loads(response.text))
# attendance_id = 

# prepare headers for http request
# content_type = 'json'
# headers = {'content-type':content_type}

# config = {'Username':'LMSAppUser', 'Password':'LMSAppUserPwd'}

# response = requests.post(test_url, data=config, headers=headers)
# print(response)
# print(json.loads(response.text))