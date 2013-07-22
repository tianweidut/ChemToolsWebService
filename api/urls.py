# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''
from django.conf.urls.defaults import *
from api.apis import *

entry_resource = UserResource()

urlpatterns = patterns('',
        (r'', include(entry_resource.urls)))
