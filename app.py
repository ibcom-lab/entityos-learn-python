import entityos_cloud as cloud
import entityos_app as app

def start(data):
    searchArgs = dict()
    searchArgs['object'] = 'contact_person'
    searchArgs['fields'] = ['firstname']
    searchArgs['row'] = 999

    responseData = cloud.search(**searchArgs)
    print(responseData)

# replace settings-private.json with the name of your settings file
# i.e. edit settings.json with your logon details and can then do as
# file='settings.json'

cloud.init(file='settings-private.json')
cloud.logon(oncomplete=start)

