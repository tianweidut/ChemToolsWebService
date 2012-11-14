# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''

from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    complete = models.BooleanField(default=False, null=False)
    
    def __unicode__(self):
        return self.name