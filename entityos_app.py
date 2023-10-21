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

app_data = dict()

def init(**kwargs):
    with open('settings.json', 'r') as file:
        settings = file.read()
        app_data['settings'] = json.loads(settings)
        return app_data['settings']

# Controllers

def add(**kwargs):
    # Add function to controller
    print(kwargs)

def invoke(**kwargs):
    # Invoke controller function to controller
    print(kwargs)

# Data

def clear(**kwargs):
    # Clear data based on scope and context
    print(kwargs)

def set(**kwargs):
    # Set data based on scope and context
    print(kwargs)

def get(**kwargs):
    # Get data based on scope and context
    print(kwargs)


