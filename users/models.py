# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)