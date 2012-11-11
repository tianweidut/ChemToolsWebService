# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    machinecode = models.CharField(max_length = 60)
    
    def __unicode__(self):
        return '%s' %(self.user)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    