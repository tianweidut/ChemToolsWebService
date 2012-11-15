# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''

from django.db import models
from users.models import UserProfile

class ActiveKeyInfo(models.Model):
    """
    Active Key base table
    """
    keyID       = models.IntegerField(primary_key=True)
    keyValue    = models.CharField(max_length = 40,unique=True)
    totalCount  = models.IntegerField()
    leftCount   = models.IntegerField()
    
    def __unicode__(self):
        return self.keyid
    
class ActiveHistory(models.Model):
    """
    Active history (for calculate)
    """
    user        = models.ForeignKey(UserProfile)
    activeIP    = models.URLField()
    activeTime  = models.DateTimeField()
    antActiveIP = models.URLField()
    antActiveTime = models.DateTimeField()
    activekey   = models.ForeignKey(ActiveKeyInfo)
    
    def __unicode__(self):
        return self.user
    
class ModelInfo(models.Model):
    """
    Chemistry Models Information
    """
    modelName = models.CharField(max_length = 200)
    
    def __unicode__(self):
        return self.modelName

class CompoundInfo(models.Model):
    """
    Smiles and CAS compound
    """
    smilesInfo = models.CharField(max_length = 200,primary_key=True)
    casInfo    = models.CharField(max_length = 100)

class CompoundName(models.Model):
    """
    Smiles and CAS name compound
    """
    simlesInfo = models.ForeignKey(CompoundInfo)
    nameStr = models.CharField(max_length = 500)
    
class CalculateHistory(models.Model):
    """
    Calculte history
    """   
    user        = models.ForeignKey(UserProfile)
    calculateStartTime = models.DateTimeField()
    calculateEndTime   = models.DateTimeField(blank=True)
    paramInfo   = models.TextField(blank=True)
    result      = models.TextField(blank=True)
    isFinished  = models.BooleanField(blank=True)
    modelInfo   = models.ForeignKey(ModelInfo)
    smilesInfo  = models.ForeignKey(CompoundInfo)
    

    
    
    
    
    
    