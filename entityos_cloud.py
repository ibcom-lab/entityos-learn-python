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
    filename = kwargs.get('filename')
    obj = kwargs.get('object')
    objContext = kwargs.get('objectContext')
    isBase64 = kwargs.get('base64')
    fileType = kwargs.get('type')
    fileData = kwargs.get('fileData')
   
    # entityos_data['settings']
   
    if not isBase64:
        import base64

        with open(filename, "rb") as file:
            fileData = base64.b64encode(file.read()).decode()

    response = invoke(
        method='core_attachment_from_base64',
        data={
            'base64': fileData,
            'filename': filename,
            'object': obj,
            'objectcontext': objContext,
            'type': fileType
            })

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

def logoff():
    logoffURL = 'https://' + entityos_data['settings']['entityos']['hostname'] + '/rpc/coree/?method=CORE_LOGOFF'
    send(url=logoffURL)

def invoke(**kwargs):
    invokeArgs = dict()
    invokeArgs['data'] = kwargs.get('data')
    invokeArgs['method'] = kwargs.get('method')
    
    if not invokeArgs['method']:
        print("Error: Must provide 'method'.")
        return None
    
    endpoint = invokeArgs['method'] .split('_')[0]
    method = invokeArgs['method']

    invokeArgs['url'] = 'https://' + entityos_data['settings']['entityos']['hostname'] + '/rpc/' + endpoint + '/?method=' + method
    
    return send(**invokeArgs)

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
    saveArgs = dict()
    saveArgs['data'] = kwargs.get('data', {})
    
    if not all(key in saveArgs['data'] for key in ['id']):
        print("Error: data must contain 'id'.")
        return None

    saveArgs['object'] = kwargs.get('object')
    
    # Identify the endpoint and method based on the object type
    endpoint = saveArgs['object'].split('_')[0]
    method = saveArgs['object'].upper() + '_MANAGE'

    # Set the URL for the save operation
    saveArgs['url'] = 'https://' + entityos_data['settings']['entityos']['hostname'] + '/rpc/' + endpoint + '/?method=' + method
    
    return send(**saveArgs)


def delete(**kwargs):
    deleteArgs = dict()
    deleteArgs['data'] = dict()

    deleteArgs['data']['id'] = kwargs.get('id')
    deleteArgs['object'] = kwargs.get('object')
    
    if not deleteArgs['data']['id'] or not  deleteArgs['object']:
        print("Error: Must provide 'id' and 'objectType'.")
        return None

    deleteArgs['data']['remove'] = 1
    
    endpoint = deleteArgs['object'] .split('_')[0]
    method = deleteArgs['object'].upper() + '_MANAGE'

    deleteArgs['url'] = 'https://' + entityos_data['settings']['entityos']['hostname'] + '/rpc/' + endpoint + '/?method=' + method
    
    return send(**deleteArgs)


search_criteria = {
            'fields': [],
            'summaryFields': [],
            'filters': [],
            'sorts': [],
            'options': {},
            'customoptions': []
        }


