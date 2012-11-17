# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''

import base64
import hashlib

from piston.handler import BaseHandler
from api.models import Task

from django.test.client import Client
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate

from deps.common.chem.proto import messages_pb2
from calcore.controllers import InputProcessing 

from api.decorators import message_handler

from backend.logging import logger
from backend.fileoperator import receiveFile
from api.decorators import message_handler

class TaskHandler(BaseHandler):
    """
    only for test
    """
    model = Task
    url = 'testmodel/'
    
class DataHandler(BaseHandler):
    """
    only for test
    """
    methods_allowed = ('GET',)
    url = 'testget/'

    def read(self, request, username=None, data=None):
        return { 'user': 'tianwei', 'data_length': len('tesa') }

class FileUploadTestHandler(BaseHandler):
    """
    only for file upload test
    """
    methods_allowed = ('POST',)
    url = 'testfile/'
    
    def create(self,request):
        """
        """
        try:            
            uploadFileObj = request.FILES 
            file_obj = InputProcessing.FilesCalculate()
            
            #TODO: whether the agentID is right 
            if uploadFileObj is not None:
                #Process upload file
                fileName = receiveFile(uploadFileObj)
                
                isSuccessful, result, reason, status \
                         = file_obj.fileQuery(
                                           fullfilename = fileName,                               
                                                )
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Smile Search Error %s "%err)
 
class SmileSearchHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'smilesearch/'
    
    request_message = messages_pb2.SmileCodeSearch
    response_message = messages_pb2.SmileCodeSearchResponse 
    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        """
        try:
            if authentication_pass:
                smile_obj = InputProcessing.SmileCalculate()
                msg_resp.isSuccessful, msg_resp.result, msg_resp.reason \
                         = smile_obj.smileQuery(
                                           query = msg_recv.query,
                                           expectedEnglishName = msg_recv.expectedEnglishName                                 
                                                )
            else:
                msg_resp.isSuccessful = False
                msg_resp.result = "None"
                msg_resp.reason = "Wrong Agent ID"
                
            ret = msg_resp.SerializeToString()
            
            return ret
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Smile Search Error %s "%err)
            
class CasSearchHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'cassearch/'
    
    request_message = messages_pb2.CasCodeSearch
    response_message = messages_pb2.CasCodeSearchResponse 
    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        """
        try:
            if authentication_pass:
                cas_obj = InputProcessing.CasCalculate()
                msg_resp.isSuccessful, msg_resp.result, msg_resp.reason \
                         = cas_obj.casQuery(
                                           query = msg_recv.query,                               
                                                )
            else:
                msg_resp.isSuccessful = False
                msg_resp.result = "None"
                msg_resp.reason = "Wrong Agent ID"
                
            ret = msg_resp.SerializeToString()
            
            return ret
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Cas Search Error %s "%err)           

class FileUploadCalculateSearchHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'fileuploadcalculatesearch/'
    
    request_message = messages_pb2.FileUploadCalculate
    response_message = messages_pb2.FileUploadCalculateResponse 
    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        """
        try:
            uploadFileObj = request.FILES 

            #TODO: whether the agentID is right 
            if authentication_pass and uploadFileObj is not None:
                file_obj = InputProcessing.FilesCalculate()
                #Process upload file
                fileName = receiveFile(uploadFileObj)

                msg_resp.isSuccessful, msg_resp.result, msg_resp.reason, msg_resp.status \
                         = file_obj.fileQuery(
                                           fullfilename = fileName,                               
                                                )
            else:
                msg_resp.isSuccessful = False
                msg_resp.result = "None"
                msg_resp.reason = "Wrong Agent ID"
                msg_resp.status = "Failed"
                
            ret = msg_resp.SerializeToString()
            
            return ret
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("File Search Error %s "%err)  
      
   
class LoginHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'login/'
    
    request_message = messages_pb2.Login
    response_message = messages_pb2.LoginResponse
    
    def create(self,request):
        """
        """
        try:
            #receive message
            msg = request.POST.get('msg', None)
            
            login_msg = self.request_message()
            response = self.response_message()
            login_msg.ParseFromString(base64.b64decode(msg))
            
            #process
            user = authenticate(
                                username=login_msg.username, 
                                password=login_msg.password
                                )
            
            if user is  None:
                #Login baned
                response.agentID = "FFFF-FFFF-FFFF-FFFF"
                response.isSucceddful = False
                response.reason = "Wrong username or password"
            else:
                #Login ok
                response.agentID = user.get_profile().agentID
                response.isSucceddful = True
                response.reason = "Login Successful"

            ret = response.SerializeToString()
            
            return base64.b64encode(ret)
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Login from Client Error %s "%err)
    
class LogoutHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'logout/'
    
    request_message = messages_pb2.Logout
    response_message = messages_pb2.LogoutResponse 
    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        """
        try:
            if authentication_pass:
                msg_resp.status = "Successful Logout!"
            else:
                msg_resp.status = "Failed Logout!"
            
            ret = msg_resp.SerializeToString()
            return ret
        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Client Logout Error %s "%err)    
       
        
            
            