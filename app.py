import entityos_cloud as cloud
import entityos_app as app

def start(data):
    searchArgs = dict()
    searchArgs['object'] = 'contact_person'
    searchArgs['fields'] = ['firstname']
    searchArgs['row'] = 999

    responseData = cloud.search(**searchArgs)
    print(responseData)

cloud.init()
cloud.logon(oncomplete=start)

