from __future__ import print_function
import requests
import json
from flask import request

API_ENDPOINT = 'http://devdonation.jnms.org:10041'
post_url = API_ENDPOINT + '/api/Processor/PostAttendanceResults'

# prepare headers for http request
content_type = 'application/json'
headers = {'content-type':content_type}

data = {
  "CONTENT": [
    {
      "AttendanceId": 1737,
      "Result": "true"
    },
    {
      "AttendanceId": 1738,
      "Result": "true"
    }
  ]
}

response = requests.post(post_url, data=data, headers=headers, auth=('LMSAppUser', 'LMSAppUserPwd'))
print(response)
print(json.loads(response.text))
# print(response.headers)
