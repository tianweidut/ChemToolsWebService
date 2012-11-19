# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''

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

from api.decorators import message_handler

from backend.logging import logger
from backend.fileoperator import receiveFile
from api.decorators import message_handler

from gui.models import *
from users.models import UserProfile
from users.models import DEFAULT_ERROR_ID

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
                
            return msg_resp
            
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
                
            return msg_resp
            
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
                
            return msg_resp
            
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
                response.agentID = DEFAULT_ERROR_ID
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
            
            return msg_resp
        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Client Logout Error %s "%err)    
       
class GetLicenseInfoHandler(BaseHandler): 
    allow_method = ('POST',)
    url = 'getlicenseinfo/'
    
    request_message = messages_pb2.GetLicenseInfo
    response_message = messages_pb2.GetLicenseInfoResponse
    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp):
        """
        The function will judge the license.
        """
        try:
            #receive message
            try:
                activeInfo = ActiveKeyInfo.objects.get(keyValue=ActiveKeyInfo)
                msg_resp.IsValidated = True
                msg_resp.TotalCount = activeInfo.totalCount
                msg_resp.LeftCount = activeInfo.leftCount
            except ActiveKeyInfo.DoesNotExist:
                msg_resp.IsValidated = False
                msg_resp.TotalCount = 0
                msg_resp.LeftCount = 0
                
            return msg_resp
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("License from Client Error %s "%err)
            
class CheckUsernameHandler(BaseHandler): 
    allow_method = ('POST',)
    url = 'checkusername/'
    
    request_message = messages_pb2.CheckUsername
    response_message = messages_pb2.CheckUsernameResponse
    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp):
        """
        The function will judge the license.
        """
        try:
            #receive message
            username_unique = True
            email_unique = True
            
            try:
                user = UserProfile.objects.get(username=msg_recv.Username)
                if user.email != msg_recv.Email:
                    email_unique = False
            except UserProfile.DoesNotExist:
                username_unique = False
                try:
                    user = UserProfile.objects.get(email=msg_recv.Email)
                    email_unique = False
                except UserProfile.DoesNotExist:
                    pass
                    
            msg_resp.IsValidatedUserName = username_unique
            msg_resp.IsValidatedEmail = email_unique
            
            return msg_resp
                        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error(" Username or Email check Error %s "%err)

class RegisterHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'register/'
    
    request_message = messages_pb2.Regist
    response_message = messages_pb2.RegistResponse
    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp):
        """
        The function will judge the license.
        """
        try:
            try:
                licenseobj = ActiveKeyInfo.objects.get(keyValue= msg_recv.LicenseStr)
                try:
                    from django.contrib.auth.models import User
                    new_user = User.objects.create_user(username=msg_recv.Username,
                                                         email =msg_recv.Email, 
                                                         password =msg_recv.Password)
                    new_user.is_active = True
                    new_user.save()
                    new_user.get_profile().machinecode = msg_recv.MachineCode
                    new_user.get_profile().agentID = str(uuid.uuid4())  # create uuid for every user profile
                    new_user.get_profile().workunit = msg_recv.WorkUnit
                    new_user.get_profile().address = msg_recv.Address
                    new_user.get_profile().telephone = msg_recv.Tel
                    new_user.get_profile().save()
                    
                    msg_resp.agentID =  new_user.get_profile().agentID 
                    msg_resp.isSuccessful = True
                    msg_resp.reason = "Successful"
                except Exception,err:
                    msg_resp.agentID = DEFAULT_ERROR_ID
                    msg_resp.isSuccessful = False
                    msg_resp.reason = "Wrong UserName or Email!!!"
            except ActiveKeyInfo.DoesNotExist:
                
                msg_resp.agentID = DEFAULT_ERROR_ID
                msg_resp.isSuccessful = False
                msg_resp.reason = "Wrong License!!!"
                        
            return msg_resp
                
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error(" Register Info Error %s "%err)          
            
class GetAllCalculateHandler(BaseHandler):  
    allow_method = ('POST',)
    url = 'getallcalculate/'

    request_message = messages_pb2.GetAllCalculate
    response_message = messages_pb2.GetAllCalulateResponse

    
    @message_handler(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        The function will get the history of calculate.
        """
        try:
            if authentication_pass:
                msg_resp =  self.find(msg_recv.agentID,msg_resp)
                msg_resp.isSuccessful = True
            else:
                msg_resp.isSuccessful = False
                msg_resp.Count = 0
            
            return msg_resp
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error(" Get Calculate Info Error %s "%err)    
    
    def find(self,agentID,msg_resp):
        """
        Find and return Calculated Info [repeated]
        """
        #Get Entity by agentID
        resultSets = CalculateHistory.objects.filter(user__agentID = agentID)
        for result in resultSets:
            calculateInfo = msg_resp.History.add()
            calculateInfo.CalStarttime = str(result.calculateStartTime)
            calculateInfo.CalEndtime = str(result.calculateEndTime)
            calculateInfo.IsFinished = result.isFinished
            calculateInfo.Param = result.paramInfo
            calculateInfo.Result = result.result
            
            calculateInfo.Smiles = result.smilesInfo.smilesInfo
            calculateInfo.CAS = result.smilesInfo.casInfo
            
            nameSets = CompoundName.objects.filter(simlesInfo=result.smilesInfo.pk,isDefault=True)
            for nameSet in nameSets:
                if nameSet.languageID.languageStr == Chinese_Name_Label:
                    calculateInfo.ChName = nameSet.nameStr
                elif nameSet.languageID.languageStr == English_Name_Label:
                    calculateInfo.EnName = nameSet.nameStr

        msg_resp.Count = len(resultSets)      
        
        return msg_resp
    
    
    
    
    
    
    
    
    
    
             
            
            