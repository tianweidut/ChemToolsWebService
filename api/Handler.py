# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''

import logging
import time
import base64
import hashlib

from piston.handler import BaseHandler
from api.models import Task

from django.test.client import Client
from django.http import HttpResponse
from django.conf import settings

from deps.common.chem.proto import messages_pb2

class TaskHandler(BaseHandler):
    model = Task
    
class DataHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request, username=None, data=None):
        return { 'user': 'tianwei', 'data_length': len('tesa') }
    
      
class TestHandler(BaseHandler):
    allow_methods = ('POST','GET')
    
    request_message = messages_pb2.RegisterAgent
    response_message = messages_pb2.RegisterAgentResponse
    
    def read(self,request):
        """
        """
        try:
            return request.META['REMOTE_ADDR']
        except Exception,err:
            import pdb;
            print pdb.traceback
            logging.error("Register Error%s"%err)
        
    def create(self,request):
        """
        """
        try:
            #receive message
            msg = request.POST.get('msg', None)
            agent_ip = request.META['REMOTE_ADDR']
            
            register_msg = messages_pb2.RegisterAgent()
            register_msg.ParseFromString(base64.b64decode(msg))
            
            response = messages_pb2.RegisterAgentResponse()
            
            #process
            ret = ""
            response.agentID = " for test " + register_msg.information
            response.information = register_msg.versionNo
            ret = response.SerializeToString()
            
            return base64.b64encode(ret)
            #return base64.b64encode("Test")
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logging.error("Register Error %s "%err)
            
            
            
            