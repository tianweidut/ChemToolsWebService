# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from const.models import *

DEFAULT_CREATE_ID = "0000-0000"
DEFAULT_ERROR_ID = "FFFF-FFFF"

class UserGrade(models.Model):
    """
    User Grade
    """
    grade = models.ForeignKey(LevelGrageCategory, unique=True,
                              verbose_name="Level Grade")
    account = models.ForeignKey(LevelAccountCategory, unique=True,
                                verbose_name="Level account")
    bill = models.ForeignKey(LevelBillCategory, unique=True,
                             verbose_name="Level bill")
    total_num = models.IntegerField(blank=False, verbose_name="total numbers")

    def __unicode__(self):
        return '%s' % (self.grade)


class UserProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    user = models.OneToOneField(User)
    machinecode = models.CharField(max_length=100)
    agentID = models.CharField(max_length=40, default=uuid.uuid4(), unique=True)
    workunit = models.CharField(max_length=2000, blank=True)
    address = models.CharField(max_length=2000, blank=True)
    telephone = models.CharField(max_length=100, blank=True)
    remaining_num = models.IntegerField(blank=False, verbose_name="remaining numbers")
    user_grade = models.ForeignKey(UserGrade, blank=False, verbose_name="user grade")

    def __unicode__(self):
        return '%s' % (self.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
