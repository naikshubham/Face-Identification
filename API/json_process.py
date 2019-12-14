import json

data = json.loads(open('data.json').read())

result = {"CONTENT":[]}

for d in data['CONTENT']:
    result['CONTENT'].append({'AttendanceId':d['AttendanceId'], 'Result':'true'})

# print(data)
print('result->', result)