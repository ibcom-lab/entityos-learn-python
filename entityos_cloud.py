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
    url = kwargs.get('url')
    data = kwargs.get('data', {})
    contenttype = kwargs.get('contenttype')

    if (contenttype == None):
        contenttype = 'application/x-www-form-urlencoded'
    
    headers = dict()
    headers['auth-sid'] = entityos_data['session']['sid']
    headers['auth-logonkey'] =  entityos_data['session']['logonkey']
    headers['content-type'] = contenttype

    data['sid'] = entityos_data['session']['sid']
    data['logonkey'] =  entityos_data['session']['logonkey']

    print('#SEND DATA:')
    print(data)

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
        logonAuthResponseData = response.json();
        print('#LOGON AUTH RESPONSE:')
        print(logonAuthResponseData)
        entityos_data['session']['logonkey'] = logonAuthResponseData.get('logonkey')
       
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
            logonResponseData = response.json()
            entityos_data['session']['logonkey'] = logonResponseData.get('logonkey')
            entityos_data['session']['sid'] = logonResponseData.get('sid')

            if (oncomplete == None):
                return logonResponseData
            else:
                oncomplete(logonResponseData)

        else:
            print("ER:", response.status_code)

    else:
         print("ER:", response.status_code)

def logoff(**kwargs):
    print(kwargs)

def invoke(**kwargs):
    print(kwargs)

def search(**kwargs):
    sendArgs = dict()
    sendArgs['data'] = dict()
    sendArgs['data']['criteria'] = dict(search_criteria)

    sendArgs['data']['object'] = kwargs.get('object')

    if (kwargs.get('fields') != None):
         sendArgs['data']['criteria']['fields'] = list(map(lambda f: {'name': f}, kwargs['fields']))

    if (kwargs.get('summaryFields') != None):
         sendArgs['data']['criteria']['summaryFields'] = kwargs['summaryFields']

    if (kwargs.get('filters') != None):
         sendArgs['data']['criteria']['filters'] = kwargs['filters']

    if (kwargs.get('options') != None):
         sendArgs['data']['criteria']['options'] = kwargs['options']

    if (kwargs.get('customOptions') != None):
         sendArgs['data']['criteria']['customOptions'] = kwargs['customOptions']

    if (kwargs.get('rows') != None):
         sendArgs['data']['criteria']['rows'] = kwargs['rows']

    endpoint = sendArgs['data']['object'].split('_')[0]

    sendArgs['url'] = 'https://' + entityos_data['settings']['entityos']['hostname'] + '/rpc/' + endpoint + '/?method=' + sendArgs['data']['object'].upper() + '_SEARCH'

    sendArgs['data']['criteria'] = json.dumps(sendArgs['data']['criteria'])
  
    return send(**sendArgs)

def save(**kwargs):
    print(kwargs)

def delete(**kwargs):
    print(kwargs)

search_criteria = {
            'fields': [],
            'summaryFields': [],
            'filters': [],
            'sorts': [],
            'options': {},
            'customoptions': []
        }


