import entityos_cloud as cloud
import entityos_app as app

def init2(**kwargs):
   print(kwargs)
   print(kwargs['arg1'])

#init2(**{'arg1': 'test'})
#init2(arg1 = 'test')

#print(cloud.logon())
#print(app.invoke())

def func2(oncomplete):
   oncomplete(arg1 = 'test')

func2(init2)
