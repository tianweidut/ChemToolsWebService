# -*- coding: UTF-8 -*-
'''
Created on 2012-11-20

@author: tianwei
'''
from backend.logging import logger

class Login(object):
    __dct__ = ('username','password',)
    
    username =None
    password = None
    
class LoginResponse(object):
    __dct__ = ('agentID','isSucceddful','reason',)  
    
    agentID = None
    isSuccessful = None
    reason = None  

class SmileCodeSearch(object):  
    __dct__ = ('agentID','query','expectedEnglishName',) 
    
    agentID = None
    query = None
    expectedEnglishName= None


class SmileCodeSearchResponse(object):   
    __dct__ = ('isSucceddful','result','reason',) 
    
    isSuccessful = None
    result = None
    reason = None


class CasCodeSearch(object): 
    __dct__ = ('agentID','query',)    
    
    agentID = None
    query = None

class CasCodeSearchResponse(object):    
    __dct__ = ('isSucceddful','result','reason',) 
    
    isSuccessful = None
    result = None
    reason = None

class FileUploadCalculate(object):   
    __dct__ = ('agentID',)
    
    agentID = None
    
class FileUploadCalculateResponse(object):    
    __dct__ = ('isSucceddful','result','reason',) 
    
    isSuccessful = None
    result= None
    reason= None

class Logout(object): 
    __dct__ = ('agentID',)   
    
    agentID = None

class LogoutResponse(object): 
    __dct__ = ('status',)   
    
    status = None
    
class GetLicenseInfo(object):   
    __dct__ = ('licenseStr',) 
    licenseStr = None  

class GetLicenseInfoResponse(object):    
    __dct__ = ('isValidated','totalCount','leftCount',) 
    
    isValidated = None
    totalCount = None
    leftCount = None

class CheckUsername(object): 
    __dct__ = ('username',)  
    
    username = None
    
class CheckUsernameResponse(object): 
    __dct__ = ('isValidatedUserName',)   
    
    isValidatedUserName = None

class CheckEmail(object):
    __dct__ = ('email',)
    
    email = None
    
class CheckEmailResponse(object): 
    __dct__ = ('isValidatedEmail',)   
    
    isValidatedEmail = None    

class Regist(object):  
    __dct__ = ('licenseStr','username','password','email','tel','workUnit','address','machineCode',)   
    
    licenseStr = None 
    username  = None
    password = None
    email = None
    tel = None
    workUnit  = None
    address = None
    machineCode = None    

class RegistResponse(object):   
    __dct__ = ('agentID','isSucceddful','reason',)  
    
    agentID = None  
    isSucceddful = None 
    reason = None

class GetAllCalculate(object):  
    __dct__ = ('agentID',)  
    
    agentID = None


class CalculateInfo(object):    
    __dct__ = ('calStarttime','calEndtime','smiles','cas','chName','enName','param','result','isFinished',)     
   
    calStarttime = None 
    calEndtime = None 
    smiles= None 
    cas= None 
    chName= None 
    enName= None 
    param= None 
    result= None 
    isFinished= None 

class GetAllCalulateResponse(object): 
    __dct__ = ('isSuccessful','count','history',)  
    
    isSuccessful= None  
    count= None 
    history= None    

class GetChemistryInfo(object):
    __dct__ = ('agentID','smiles',)  
    
    agentID= None  
    smiles= None 

class GetChemistryInfoResponse(object):
    __dct__ = ('smiles','cas','names')  
    
    smiles= None  
    cas= None     
    names = None
    
class GetChemInfoName(object):
    simlesInfo = None
    nameStr = None
    languageID = None
    isDefault = None
    
def parseJsonToObject(dct,message_type):
    """
    Get dct and message_type to create the object
    """
    obj = message_type()
    for item in obj.__dct__:
        #TODO cannot solve subclass
        try:
            obj.__setattr__(item,dct[item])
        except Exception,err:
            logger.error(err)
        
    return obj
    
    
    
    
    
    
