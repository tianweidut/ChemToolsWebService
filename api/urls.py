# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''
from django.conf.urls.defaults import *
from piston.resource import Resource

from api.Handler import *

class CsrfExemptResource(Resource):
    def __init__(self,handler, authentication = None):
        super( CsrfExemptResource, self ).__init__( handler, authentication )
        self.csrf_exempt = getattr( self.handler, 'csrf_exempt', True )

task_resource = CsrfExemptResource(TaskHandler)
test_resource = CsrfExemptResource(TestHandler)
data_resource = CsrfExemptResource(DataHandler)

urlpatterns = patterns('',
   url(r'^tasks/(?P<id>\d+)$', task_resource),
   url(r'^tasks$', task_resource),
   url(r'^test$', test_resource),
   url(r'^data$', data_resource)
)