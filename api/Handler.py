# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''

import logging
import time
import base64
import hashlib
import uuid
import os

from piston.handler import BaseHandler
from api.models import Task

from django.test.client import Client
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate

from deps.common.chem.proto import messages_pb2
from calcore.controllers import InputProcessing 

from django.utils.log import getLogger
logger = getLogger('django')

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
    allow_method = ('POST')
    url = 'smilesearch/'
    
    request_message = messages_pb2.SmileCodeSearch
    response_message = messages_pb2.SmileCodeSearchResponse 
    
    def create(self,request):
        """
        """
        try:
            msg = request.POST.get('msg', None)
            
            smile_recv = self.request_message()
            smile_resp = self.response_message()
            
            smile_recv.ParseFromString(base64.b64decode(msg))   #We can add RSA algorightm
            
            smile_obj = InputProcessing.SmileCalculate()
            
            #TODO: whether the agentID is right 
            if smile_recv.agentID is not None and cmp(smile_recv.agentID,"FFFFFFFF") != 0:
                smile_resp.isSuccessful, smile_resp.result, smile_resp.reason \
                         = smile_obj.smileQuery(
                                           query = smile_recv.query,
                                           expectedEnglishName = smile_recv.expectedEnglishName                                 
                                                )
            else:
                smile_resp.isSuccessful = False
                smile_resp.result = "None"
                smile_resp.reason = "Wrong Agent ID"
                
            ret = smile_resp.SerializeToString()
            
            return base64.b64encode(ret)
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Smile Search Error %s "%err)
            
class CasSearchHandler(BaseHandler):
    allow_method = ('POST')
    url = 'cassearch/'
    
    request_message = messages_pb2.CasCodeSearch
    response_message = messages_pb2.CasCodeSearchResponse 
    
    def create(self,request):
        """
        """
        try:
            msg = request.POST.get('msg', None)
            
            cas_recv = self.request_message()
            cas_resp = self.response_message()
            
            cas_recv.ParseFromString(base64.b64decode(msg))   #We can add RSA algorightm
            
            cas_obj = InputProcessing.CasCalculate()
            
            #TODO: whether the agentID is right 
            if cas_recv.agentID is not None and cmp(cas_recv.agentID,"FFFFFFFF") != 0:
                cas_resp.isSuccessful, cas_resp.result, cas_resp.reason \
                         = cas_obj.casQuery(
                                           query = cas_recv.query,                               
                                                )
            else:
                cas_resp.isSuccessful = False
                cas_resp.result = "None"
                cas_resp.reason = "Wrong Agent ID"
                
            ret = cas_resp.SerializeToString()
            
            return base64.b64encode(ret)
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Cas Search Error %s "%err)           

class FileUploadCalculateSearchHandler(BaseHandler):
    allow_method = ('POST')
    url = 'fileuploadcalculatesearch/'
    
    request_message = messages_pb2.FileUploadCalculate
    response_message = messages_pb2.FileUploadCalculateResponse 
    
    def create(self,request):
        """
        """
        try:
            msg = request.POST.get('msg', None)
            uploadFileObj = request.FILES 

            
            file_recv = self.request_message()
            file_resp = self.response_message()
            
            file_recv.ParseFromString(base64.b64decode(msg))   #We can add RSA algorightm
            
            file_obj = InputProcessing.FilesCalculate()
            
            #TODO: whether the agentID is right 
            if file_recv.agentID is not None and cmp(file_recv.agentID,"FFFFFFFF") != 0 and uploadFileObj is not None:
                #Process upload file
                fileName = self.receiveFile(uploadFileObj)

                file_resp.isSuccessful, file_resp.result, file_resp.reason, file_resp.status \
                         = file_obj.fileQuery(
                                           fullfilename = fileName,                               
                                                )
            else:
                file_resp.isSuccessful = False
                file_resp.result = "None"
                file_resp.reason = "Wrong Agent ID"
                file_resp.status = "Failed"
                
            ret = file_resp.SerializeToString()
            
            return base64.b64encode(ret)
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("File Search Error %s "%err)  
      
   
class LoginHandler(BaseHandler):
    allow_method = ('POST')
    url = 'login/'
    
    request_message = messages_pb2.Login
    response_message = messages_pb2.LoginResponse
    
    def create(self,request):
        """
        """
        try:
            #receive message
            msg = request.POST.get('msg', None)
            
            login_msg = messages_pb2.Login()
            login_msg.ParseFromString(base64.b64decode(msg))
            
            response = messages_pb2.LoginResponse()
            
            #process
            user = authenticate(
                                username=login_msg.username, 
                                password=login_msg.password
                                )
            
            if user is  None:
                #Login baned
                response.agentID = "FFFFFFFF"
                response.isSucceddful = False
                response.reason = "Wrong username or password"
            else:
                #Login ok
                response.agentID = str(uuid.uuid4())
                response.isSucceddful = True
                response.reason = "Login Successful"

            ret = response.SerializeToString()
            
            return base64.b64encode(ret)
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Login from Client Error %s "%err)
    
    
class LogoutHandler(BaseHandler):
    allow_method = ('POST')
    url = 'logout/'
    
    request_message = messages_pb2.Logout
    response_message = messages_pb2.LogoutResponse 
    
    def create(self,request):
        """
        """
        try:
            response = messages_pb2.LogoutResponse()
            response.status = "Successful Logout!"
            
            ret = response.SerializeToString()
            return base64.b64encode(ret)
        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Client Logout Error %s "%err)    
       
def receiveFile(uploadFileObj):
        """
        upload File objects generate
        """
        try:
            for key,fileop in uploadFileObj.items():
                path = os.path.join(settings.TMP_FILE_PATH ,fileop.name)
                dest = open(path.encode('utf-8'), 'wb+')
                if fileop.multiple_chunks:
                    for c in fileop.chunks():
                        dest.write(c)
                else:
                    dest.write(fileop.read())
                dest.close()
                
            return path
                        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Smile Search Error %s "%err)
            
            
            
            