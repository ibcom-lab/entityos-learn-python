import entityos_cloud as cloud
import entityos_app as app

def start(data):
    print(data)
    search = dict()
    search['object'] = 'contact_person'
    search['fields'] = ['firstname']
    search['row'] = 999
    print(search)

    cloud.search(search)

cloud.init()
cloud.logon(oncomplete=start)

