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

from django.test.client import Client
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate

from deps.common.chem.json import message_json as messages_pb2
from calcore.controllers import InputProcessing

from api.decorators import message_handler

from backend.logging import logger
from backend.fileoperator import receiveFile
from api.decorators import message_handler, message_handler_json

from users.models import *
from users.models import UserProfile
from users.models import DEFAULT_ERROR_ID


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
    
    @message_handler_json(request_message,response_message)
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
    
    @message_handler_json(request_message,response_message)
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
    
    @message_handler_json(request_message,response_message)
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

                msg_resp.isSuccessful, msg_resp.result, msg_resp.reason \
                         = file_obj.fileQuery(
                                           fullfilename = fileName,                               
                                                )
            else:
                msg_resp.isSuccessful = False
                msg_resp.result = "None"
                msg_resp.reason = "Wrong Agent ID"
                
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
    
    @message_handler_json(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        """
        try:
            #process
            user = authenticate(
                                username=msg_recv.username, 
                                password=msg_recv.password
                                )
            
            if user is  None:
                #Login baned
                logger.debug("----------Failed------------%s,%s"%(msg_recv.username,msg_recv.password))
                msg_resp.agentID = DEFAULT_ERROR_ID
                msg_resp.isSuccessful = False
                msg_resp.reason = "Wrong username or password"
            else:
                #Login ok
                logger.debug("----------Successful------------%s,%s"%(msg_recv.username,msg_recv.password))
                msg_resp.agentID = user.get_profile().agentID
                msg_resp.isSuccessful = True
                msg_resp.reason = "Login Successful"

            return msg_resp
            
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Login from Client Error %s "%err)
    
class LogoutHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'logout/'
    
    request_message = messages_pb2.Logout
    response_message = messages_pb2.LogoutResponse 
    
    @message_handler_json(request_message,response_message)
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
    
    @message_handler_json(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        The function will judge the license.
        """
        try:
            #receive message
            try:
                activeInfo = ActiveKeyInfo.objects.get(keyValue=msg_recv.licenseStr)
                msg_resp.isValidated = True
                msg_resp.totalCount = activeInfo.totalCount
                msg_resp.leftCount = activeInfo.leftCount
            except ActiveKeyInfo.DoesNotExist:
                msg_resp.isValidated = False
                msg_resp.totalCount = 0
                msg_resp.leftCount = 0
                
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
    
    @message_handler_json(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        The function will judge the license.
        """
        try:
            #receive message        
            username_unique = True
            
            try:
                user = UserProfile.objects.get(user__username=msg_recv.username)
            except UserProfile.DoesNotExist:
                username_unique = False
                    
            msg_resp.isValidatedUserName = username_unique
            
            return msg_resp
                        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error(" Username or Email check Error %s "%err)

class CheckEmailHandler(BaseHandler): 
    allow_method = ('POST',)
    url = 'checkemail/'
    
    request_message = messages_pb2.CheckEmail
    response_message = messages_pb2.CheckEmailResponse
    
    @message_handler_json(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        The function will judge the license.
        """
        try:
            #receive message
            email_unique = True
            
            try:
                user = UserProfile.objects.get(user__email=msg_recv.email)
            except UserProfile.DoesNotExist:
                email_unique = False
                    
            msg_resp.isValidatedEmail = email_unique
            
            return msg_resp
                        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("Email check Error %s "%err)

class RegisterHandler(BaseHandler):
    allow_method = ('POST',)
    url = 'register/'
    
    request_message = messages_pb2.Regist
    response_message = messages_pb2.RegistResponse
    
    @message_handler_json(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass):
        """
        The function will judge the license.
        """
        try:
            try:
                licenseobj = ActiveKeyInfo.objects.get(keyValue= msg_recv.licenseStr)
                try:
                    from django.contrib.auth.models import User
                    new_user = User.objects.create_user(username=msg_recv.username,
                                                         email =msg_recv.email, 
                                                         password =msg_recv.password)
                    new_user.is_active = True
                    new_user.save()
                    new_user.get_profile().address = msg_recv.address
                    new_user.get_profile().machinecode = msg_recv.machineCode
                    new_user.get_profile().agentID = str(uuid.uuid4())  # create uuid for every user profile
                    new_user.get_profile().workunit = msg_recv.workUnit
                    new_user.get_profile().telephone = msg_recv.tel
                    new_user.get_profile().save()
                    
                    msg_resp.agentID =  new_user.get_profile().agentID 
                    msg_resp.isSuccessful = True
                    msg_resp.reason = "Successful"
                    
                    #TODO Active in ActiveHistory!!!
                except Exception,err:
                    msg_resp.agentID = DEFAULT_ERROR_ID
                    msg_resp.isSucceddful = False
                    msg_resp.reason = "Wrong UserName or Email!!! %s" % str(err)
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

    @message_handler_json(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass=True):
        """
        The function will get the history of calculate.
        """
        try:
            if authentication_pass:
                logger.debug("---------Successful-----------")
                msg_resp =  self.find(msg_recv.agentID,msg_resp)
                msg_resp.isSuccessful = True
                self.testPrint(msg_resp)
            else:
                logger.debug("---------Failed-----------")
                msg_resp.isSuccessful = False
                msg_resp.count = 0
            
            return msg_resp
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error(" Get Calculate Info Error %s "%err)    
    
    def testPrint(self,response):
        """
        Only for test 
        """
        logger.debug("---------------GetAllCalculateHandler start--------------")
        for msg_resp in response.history:
            logger.debug("CalStarttime: %s CalEndtime: %s" %(msg_resp.calStarttime,msg_resp.calEndtime))
            logger.debug("isFinished: %s" % str(msg_resp.isFinished))
            logger.debug("Param %s, Result :%s" %(msg_resp.param, msg_resp.result))
            logger.debug("Smiles %s ,CAS %s " %(msg_resp.smiles,msg_resp.cas))
            logger.debug("Chinese: %s, English %s" %(msg_resp.chName,msg_resp.enName))
        logger.debug("---------------GetAllCalculateHandler end--------------")
    
    def find(self,agentID,msg_resp):
        """
        Find and return Calculated Info [repeated]
        """
        #Get Entity by agentID
        import time
        resultSets = CalculateHistory.objects.filter(user__agentID = agentID)
        msg_resp.count = len(resultSets) 
        msg_resp.history = [None] * msg_resp.count      
        cnt = 0
        for result in resultSets:
            msg_resp.history[cnt] = messages_pb2.CalculateInfo()
            msg_resp.history[cnt].calStarttime = str(result.calculateStartTime)
            msg_resp.history[cnt].calEndtime = str(result.calculateEndTime)#.strftime('%Y-%m-%d %X')
            msg_resp.history[cnt].isFinished = result.isFinished
            msg_resp.history[cnt].param = result.paramInfo
            msg_resp.history[cnt].result = result.result
            
            msg_resp.history[cnt].smiles = result.smilesInfo.smilesInfo
            msg_resp.history[cnt].cas = result.smilesInfo.casInfo
            
            
            nameSets = CompoundName.objects.filter(simlesInfo=result.smilesInfo.pk,isDefault=True)
            for nameSet in nameSets:
                if nameSet.languageID.languageStr == Chinese_Name_Label:
                    msg_resp.history[cnt].chName = nameSet.nameStr 
                elif nameSet.languageID.languageStr == English_Name_Label:
                    msg_resp.history[cnt].enName = nameSet.nameStr
            
            cnt = cnt +1 
        
        return msg_resp
    
class GetChemistryInfoHandler(BaseHandler):  
    allow_method = ('POST',)
    url = 'getchemistryinfo/'

    request_message = messages_pb2.GetChemistryInfo
    response_message = messages_pb2.GetChemistryInfoResponse

    @message_handler_json(request_message,response_message)
    def create(self,request,msg_recv,msg_resp,authentication_pass=True):
        """
        The function will get the name of Chemistry.
        """        
        try:
            logger.debug("------------%s----------------"%(msg_recv.smiles))
            chemInfo = CompoundInfo.objects.get(smilesInfo=msg_recv.smiles)
            msg_resp = self.GetChemistryInfoDetails(chemInfo,msg_resp,msg_recv.smiles)
            msg_resp.smiles = msg_recv.smiles
        except CompoundInfo.DoesNotExist:
            msg_resp.smiles = msg_recv.smiles
            msg_resp.cas = None
            msg_resp.names = None
        
        return msg_resp
    
    def GetChemistryInfoDetails(self,chemInfo,msg_resp,simles):
        """
        """
        msg_resp.cas = chemInfo.casInfo
        msg_resp.names = []
        
        for result in [item for item in CompoundName.objects.filter(simlesInfo = chemInfo)] :
            obj = messages_pb2.GetChemInfoName()
            obj.simlesInfo = simles
            obj.nameStr = result.nameStr
            obj.languageID = result.languageID.pk
            obj.isDefault = result.isDefault
                        
            msg_resp.names.append(obj)
        
        logger.debug("----------------------test--------------------")
        for i in  msg_resp.names:
            logger.debug(i.simlesInfo)
            logger.debug(i.nameStr)
            logger.debug(i.languageID)
            logger.debug(i.isDefault)
        logger.debug("----------------------end--------------------")
        
        return msg_resp
            
            
            
        
            
    
    
    
    
             
            
            
