import requests
import json

# Standard Methods:
# init
# cloud:    logon | logoff | send | invoke | create(save,update) | delete | retrieve(search,query)
# _util:    controller: add | invoke
#           data: reset | clear | set | get
#           attach (upload): 

# init | add | invoke | set | get
# cloud: auth | deuth | search | save | upload
# util: send

# https://chat.openai.com/share/98bd2a20-10e0-4c2b-8dc3-7df6e5988224

# url = 'https://' + data['settings']['entityos']['hostname'] + '/rpc/logon/?method=LOGON_GET_USER_AUTHENTICATION_LEVEL'

def get_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return response.json()

# Replace 'your_api_url_here' with the actual URL of the web service you want to access
url = 'https://api.entityos.cloud/rpc/logon/?method=LOGON'
#data = get_data(url)
#print(data)

with open('settings.json', 'r') as file:
    content = file.read()
    print(content)
    settings = json.loads(content)

print(settings)

import hashlib

def hash_data(data):
    result = hashlib.md5(data.encode()).hexdigest()
    return result

# LOGON AUTH LEVEL

logonAuthData = dict()

logonAuthData['method'] = 'LOGON_GET_USER_AUTHENTICATION_LEVEL'
logonAuthData['logon'] = settings['entityos']['logon']
logonAuthData['passwordhash'] = hash_data(settings['entityos']['logon'] + settings['entityos']['password'])

print()
print(logonAuthData)

logonURL = 'https://' + settings['entityos']['hostname'] + '/rpc/logon/?method=LOGON_GET_USER_AUTHENTICATION_LEVEL'
response = requests.post(logonURL, data=logonAuthData)

if response.status_code == 200:
    responseData = response.json();
    print()
    print("Success:", responseData)
    logonKey = responseData['logonkey']

else:
    print("Failed:", response.status_code)


# LOGON

logonData = dict()

logonData['method'] = 'LOGON'
logonData['logon'] = settings['entityos']['logon']
logonData['password'] = settings['entityos']['password']
logonData['logonkey'] = logonKey
logonData['passwordhash'] = hash_data(logonData['logon'] + logonData['password'])

print()
print(logonData)

logonURL = 'https://' + settings['entityos']['hostname'] + '/rpc/logon/?method=LOGON'

response = requests.post(logonURL, data=logonData)
if response.status_code == 200:
    print()
    print("Success:", response.json())

else:
    print("Failed:", response.status_code)