# coding: UTF-8
'''
Created on 2013-05-20

@author: tianwei

Desc: dict table
'''

import datetime
import uuid

from django.db import models
from django.conf import settings

from const.models import *
from const import *
from users.models import UserProfile

def get_sid():
    return str(uuid.uuid4())


class SuiteTask(models.Model):
    """
    A group of task, which defined the one calculate submit
    """
    sid = models.CharField(unique=True, blank=False, max_length=50,
                           verbose_name="id", primary_key=True,
                           default=get_sid)
    user = models.ForeignKey(UserProfile, blank=False, verbose_name="user")
    smiles = models.CharField(max_length=2000, blank=True,
                              verbose_name="smiles input")
    total_tasks = models.IntegerField(blank=False, verbose_name="total tasks")
    has_finished_tasks = models.IntegerField(blank=False, default=0,
                                             verbose_name="Finished number")
    start_time = models.DateTimeField(blank=False,
                                      default=lambda: datetime.datetime.now())
    end_time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=2000, blank=True)
    notes = models.CharField(max_length=5000, blank=True)
    status = models.ForeignKey(StatusCategory, blank=False,
                               default=STATUS_UNDEFINED)
    models_str = models.CharField(max_length=50, blank=True)
    models_category_str = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Suite Task"
        verbose_name_plural = "Suite Task"

    def __unicode__(self):
        return self.sid


class MolFile(models.Model):
    """
    Mol File, which can process upload files,
    draw chem structure files, smiles convert files
    """
    fid = models.CharField(max_length=50, primary_key=True, blank=False,
                           default=get_sid)
    sid = models.ForeignKey(SuiteTask, blank=False)
    name = models.CharField(max_length=200, blank=False)
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH+"/%Y/%m/%d")
    upload_time = models.DateTimeField(blank=True, default=lambda:datetime.datetime.now())
    file_size = models.CharField(max_length=50, blank=True, default=None)
    file_type = models.CharField(max_length=10, blank=False)
    file_source = models.ForeignKey(FileSourceCategory, blank=False)

    def __unicode__(self):
        return self.name


class SingleTask(models.Model):
    """
    Every specific task
    """
    sid = models.ForeignKey(SuiteTask, blank=False)
    pid = models.CharField(max_length=50, unique=True, blank=False,
                           primary_key=True, default=get_sid)
    temperature = models.FloatField(blank=True, default=0.0)
    humidity = models.FloatField(blank=True, default=0.0)
    other = models.FloatField(blank=True, default=0.0)
    calculate_mol = models.OneToOneField(MolFile, blank=False)
    model = models.ForeignKey(ModelCategory, blank=False)
    results = models.TextField(blank=True, null=None)
    status = models.ForeignKey(StatusCategory, blank=False,
                               default=STATUS_WORKING)

    class Meta:
        verbose_name = "Single Task"
        verbose_name_plural = "Single Task"

    def __unicode__(self):
        return self.sid.name


class ProcessedFile(models.Model):
    """
    Temp File
    """
    fid = models.CharField(max_length=50, unique=True, blank=False,
                           primary_key=True, default=get_sid)
    title = models.CharField(max_length=60, blank=False)
    file_type = models.CharField(max_length=10, blank=False)
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH+"/%Y/%m/%d")
    #sid = models.CharField(blank=True, max_length=50)

    def __unicode__(self):
        return self.title
