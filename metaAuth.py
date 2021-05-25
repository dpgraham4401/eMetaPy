# metaAuth.py
import sys, requests, json

if not sys.version_info > (2, 7):
    print('error: python version 2 not supported')
    sys.exit(1)
elif not sys.version_info >= (3, 5):
    print('warning: Python >= 3.5 not supported, proceeding')

baseUrl = 'https://rcraquery.epa.gov/metabase'
authUrl = baseUrl + '/api/session'
print(authUrl)

metaData = json.dumps({'username': 'Graham.David@epa.gov', 'password': 'G@ndolf4401'})

metaHead = {'Content-Type': 'application/json'}

res = requests.post(authUrl, data=metaData, headers=metaHead)

print(res.json)
print(res.text)

data = res.json()
print(data['id'])
