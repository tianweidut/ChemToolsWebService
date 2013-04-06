# -*- coding: UTF-8 -*-
'''
Created on 2012-11-14

@author: tianwei
'''

from django.db import models

class CasModel(models.Model):
    name = models.CharField(max_length=300)
    value = models.CharField(max_length=500)
    
class SmileModel(models.Model):
    name = models.CharField(max_length=300)
    value = models.CharField(max_length=500)