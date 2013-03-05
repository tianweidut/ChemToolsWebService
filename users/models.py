# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

DEFAULT_CREATE_ID = "0000-0000"
DEFAULT_ERROR_ID = "FFFF-FFFF"

class UserProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    user = models.OneToOneField(User)
    machinecode = models.CharField(max_length = 100)
    agentID = models.CharField(max_length = 40,default = uuid.uuid4(),unique=True)         #When the userProfile is created,agentId will be created automatically.
    workunit = models.CharField(max_length = 2000,blank=True)
    address  = models.CharField(max_length = 2000,blank=True)
    telephone = models.CharField(max_length = 100, blank=True)
    
    def __unicode__(self):
        return '%s' %(self.user)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
