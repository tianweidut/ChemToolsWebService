# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: sytmac
'''

import sys
sys.path.append("/usr/local/lib/")

import openbabel,pybel
import threading

from  calcore.controllers.MolToGjfAndMop import *

from django.utils.log import getLogger
logger = getLogger('django')


class CasCalculate:
    isSuccessful = True
    reason = "None"
    result = "None" 
    
    def casQuery(self,query):
        """
        middle-ware will call this function for cas query 
        """
        #TODO: mysql models
        self.result = "None"
        self.reason = "None"
        self.isSuccessful = True
        
        return (self.isSuccessful,self.result,self.reason)
    
class SmileCalculate:
    isSuccessful = True
    reason = "None"
    result = "None"
    
    def smileQuery(self,query,expectedEnglishName):
        """
        middle-ware will call this function for smile query 
        """
        #TODO: mysql models
        self.result = "None"
        self.reason = "None"
        self.isSuccessful = True        
        '''
        try:
            mymol=pybel.readstring('smi',str(smile_info["smile"]))
            mymol.addh()
            mymol.make3D()
            mymol.write('mol',str(smile_info["smile_name"])+".mol",overwrite=True)
        except(IOError):
            return "your input smile is invalid"
        
        return smile_info["smile_name"] 
        '''
        return (self.isSuccessful,self.result,self.reason)
             
class FilesCalculate:
    isSuccessful = True
    reason = "None"
    result = "None"
    status = "None"
    
    def fileQuery(self,fullfilename,filetype=None):
        """
        middle-ware will call this function for File query 
        """
        self.isSuccessful = True
        self.reason = "None"
        self.result = "None"
        self.status = "file upload sucess"

        try:
            self.InputWithUploadFile(fullfilename)  
        except Exception,err:
            self.isSuccessful = False
            self.reason = str(err)
            self.status = "file upload Failed"
            self.result = "Failed!"
        
        return (self.isSuccessful,self.result,self.reason,self.status)

    def InputWithUploadFile(self,filename):
        """
        """
        #split filename
        filename = os.path.basename(filename)
        
        fileExt=filename.split('.')[-1]
        if cmp(fileExt,'gjf')==0:
            logger.debug('input gjf file %s'%filename)
            #GaussianExecute.GuassianDisposal(filename)
        elif cmp(fileExt,'mop')==0:
            logger.debug('input mop file %s'%fileExt)   
            #MopacExecute.DealWithMopac(filename) 
        # when mol file is uploaded ,we start 3 thread to  act 
        # using Dragon Mopac and Gaussian respectively        
        elif cmp(fileExt,'mol')==0:
            #DragonExecute.DragonDisposal(filename)
            MolToGjfAndMop(filename)
            gjf_filename=filename.split('.')[0]+'.gjf'
            #GaussianThread=threading.Thread(target=GaussianExecute.GuassianDisposal,args=(gjf_filename,))
            #GaussianThread.start() 
            mop_filename=filename.split('.')[0]+'.mop'
            #MopacThread=threading.Thread(target=MopacExecute.DealWithMopac,args=(mop_filename,))
            #MopacThread.start()
            logger.debug('input mol file %s'%filename)
        else:
            logger.info('illegal input file formation')
