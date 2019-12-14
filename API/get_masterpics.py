import urllib.request
import os 
import pandas as pd 

path = './master/'
employee_id_path = './tables/employee_id.csv'

data = pd.read_csv(employee_id_path, na_values='n\a')
data = data.dropna(axis=0)
employee_id_list = list(data['EmployeeId'].apply(lambda x:int(x)))
# print(employee_id_list)

if not os.path.exists(path):
    os.mkdir(path)

employee_id = 0

for employee_id in employee_id_list:
    try:
        img_url = "http://devdonation.jnms.org:10041/apk/getpicof?employeeid=" + str(employee_id)
        # print(img_url)
        urllib.request.urlretrieve(img_url, path+str(employee_id)+'.jpg')
    except Exception as e:
        print(repr(e))