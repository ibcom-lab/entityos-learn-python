import requests
import json
import entityos_util as util

entityos_data = dict()

def init(**kwargs):
    with open('settings.json', 'r') as file:
        settings = file.read()
        entityos_data['settings'] = json.loads(settings)
        entityos_data['session'] = dict()
        print(entityos_data)
        return entityos_data['settings']

def send(**kwargs):
    print(kwargs)

    url = kwargs['url']
    data = kwargs['data']
    contenttype = kwargs['contenttype']
    if (contenttype == None):
        contenttype = 'application/x-www-form-urlencoded'
    
    headers = dict()
    headers['auth-sid'] = data['session']['sid']
    headers['auth-logonkey'] =  data['session']['logonkey']
    headers['Content-Type'] = contenttype

    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        responseData = response.json();
        return responseData

    else:
       return response.status_code

def upload(**kwargs):
    print(kwargs)

def logon(**kwargs):
     # LOGON AUTH LEVEL

    oncomplete = kwargs['oncomplete']

    logonAuthData = dict()
    logonAuthData['method'] = 'LOGON_GET_USER_AUTHENTICATION_LEVEL'
    logonAuthData['logon'] = entityos_data['settings']['entityos']['logon']
    logonAuthData['passwordhash'] = util.hash(entityos_data['settings']['entityos']['logon'] + entityos_data['settings']['entityos']['password'])

    logonAuthURL = 'https://' + entityos_data['settings']['entityos']['hostname'] + '/rpc/logon/'

    response = requests.post(logonAuthURL, data=logonAuthData)

    if response.status_code == 200:
        responseData = response.json();

        
        entityos_data['session']['logonkey'] = responseData['logonkey']

        # LOGON

        logonData = dict()
        logonData['method'] = 'LOGON'
        logonData['logon'] = entityos_data['settings']['entityos']['logon']
        logonData['password'] = entityos_data['settings']['entityos']['password']
        logonData['logonkey'] = entityos_data['session']['logonkey']
        logonData['passwordhash'] = util.hash(logonData['logon'] + logonData['password'])

        logonURL = 'https://' + entityos_data['settings']['entityos']['hostname'] + '/rpc/logon/'

        response = requests.post(logonURL, data=logonData)

        if response.status_code == 200:
            data = response.json()

            if (oncomplete == None):
                return data
            else:
                oncomplete(data)

        else:
            print("ER:", response.status_code)

    else:
         print("ER:", response.status_code)

def logoff(**kwargs):
    print(kwargs)

def invoke(**kwargs):
    print(kwargs)

def search(**kwargs):
    search = dict()
    search['criteria'] = dict(search_criteria)

    # use kwargs
    # set URL etc

    send(search)

def save(**kwargs):
    print(kwargs)

def delete(**kwargs):
    print(kwargs)

search_criteria ={
            'fields': [],
            'summaryFields': [],
            'filters': [],
            'sorts': [],
            'options': {},
            'customoptions': []
        }


