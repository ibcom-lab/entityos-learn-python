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

app_controller = dict()
app_data = dict()

def init(**kwargs):
    with open('settings.json', 'r') as file:
        settings = file.read()
        app_data['settings'] = json.loads(settings)
        return app_data['settings']

# Controllers

def add(**kwargs):
    # Add function to controller
    # Name is the def name

    code = kwargs.get('code')
    if (code != None):
        exec(code, app_controller)

def invoke(**kwargs):
    # Invoke controller function to controller
    name = kwargs.get('name')
    
    if (name != None):
        app_controller[name](**kwargs)

# Data

def clear(**kwargs):
    # Clear data based on scope and context
    scope = kwargs.get('scope')
    context = kwargs.get('context')
    name = kwargs.get('name')
    
    if (scope != None):
        if (context == None):
            app_data[scope] = None
        else:
            if (name == None):
                app_data[scope][context] = None
            else:
                app_data[scope][context][name] = None


def set(**kwargs):
    # Set data based on scope and context
    scope = kwargs.get('scope')
    context = kwargs.get('context')
    name = kwargs.get('name')
    value = kwargs.get('value')
    
    if (scope != None):
        if (context == None):
            app_data[scope] = value
        else:
            if (name == None):
                app_data[scope][context] = value
            else:
                app_data[scope][context][name] = value

    return value

def get(**kwargs):
    # Get data based on scope and context
    scope = kwargs.get('scope')
    context = kwargs.get('context')
    name = kwargs.get('name')
    value = None

    if (scope != None):
        if (context == None):
            if (scope in app_data):
                value = app_data[scope]
        else:
            if (name == None):
                if (scope in app_data):
                    if (context in app_data[scope]):
                        value = app_data[scope][context]
            else:
                if (scope in app_data):
                    if (context in app_data[scope]):
                         if (name in app_data[scope][context]):
                            value = app_data[scope][context][name]

    return value


