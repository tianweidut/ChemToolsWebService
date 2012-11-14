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

ACTIVE_HANDLERS = (
          TaskHandler,
          DataHandler,
          SmileSearchHandler,
          CasSearchHandler,
          FileUploadCalculateSearchHandler,
          LoginHandler,
          LogoutHandler,
                   )

urlpatterns = patterns('',
        *[url(r'^%s/?$' %  Handler.url,CsrfExemptResource(Handler))\
          for Handler in ACTIVE_HANDLERS])
