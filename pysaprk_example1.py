import json

import requests
from requests.auth import HTTPBasicAuth

LIVY_URL="http://localhost:8998/"
LIVY_URL='https://noam-c3.azurehdinsight.net'
data = { 'kind': 'pyspark',
        'files' : 'minimal.py' ,
        'name' : 'first_test_app'
        }
        
headers = {'Content-Type': 'application/json',
           "X-Requested-By": "user"}

auth = HTTPBasicAuth('admin', '!Qq12345678')

r = requests.get(LIVY_URL + '/livy/sessions', headers=headers,
	auth = auth)
print(r.json())

print(" \nCreating a new session. posting...")
r = requests.post(LIVY_URL + '/livy/sessions', data=json.dumps(data), headers=headers,
	auth = auth)
print(str(r))

#{u'id': 1, u'state': u'idle'}
