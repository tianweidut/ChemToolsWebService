# coding: UTF-8
import datetime
import uuid

from django.db import models
from django.conf import settings

from users.models import UserProfile
from chemistry import (MODEL_ORIGIN_CHOICES,
                       MODEL_CHOICES, STATUS_CHOICES, MOL_ORIGIN_CHOICES,
                       ORIGIN_UNDEFINED, STATUS_UNDEFINED, STATUS_WORKING,
                       ORIGIN_UPLOAD)
import utils


def get_sid():
    return str(uuid.uuid4())


class ModelTypeCategory(models.Model):
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=MODEL_ORIGIN_CHOICES,
                                verbose_name=u"Calculate Model Type")

    class Meta:
        verbose_name = "计算模型类别"
        verbose_name_plural = "计算模型类别"

    def __unicode__(self):
        return self.get_category_display()


class ModelCategory(models.Model):
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=MODEL_CHOICES,
                                verbose_name=u"Calculate Model")
    origin_type = models.ForeignKey(ModelTypeCategory, blank=False)
    desc = models.TextField(blank=True)

    class Meta:
        verbose_name = "计算模型"
        verbose_name_plural = "计算模型"

    def __unicode__(self):
        return self.get_category_display()


class StatusCategory(models.Model):
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=STATUS_CHOICES,
                                verbose_name=u"计算状态")

    class Meta:
        verbose_name = "计算状态"
        verbose_name_plural = "计算状态"

    def __unicode__(self):
        return self.get_category_display()


class FileSourceCategory(models.Model):
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=MOL_ORIGIN_CHOICES,
                                default=ORIGIN_UNDEFINED)

    class meta:
        verbose_name = "文件来源"
        verbose_name_plural = "文件来源"

    def __unicode__(self):
        return self.get_category_display()


class ProcessedFile(models.Model):
    """上传及计算文件对象"""
    fid = models.CharField(max_length=50, unique=True, blank=False,
                           primary_key=True, default=get_sid)
    title = models.CharField(max_length=500, blank=False)
    file_type = models.CharField(max_length=100, blank=False)
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH)
    file_source = models.ForeignKey(FileSourceCategory,
            default=lambda: FileSourceCategory.objects.get(category=ORIGIN_UPLOAD))
    image = models.FileField(blank=True, null=True,
                             upload_to=settings.PROCESS_FILE_PATH)
    smiles = models.CharField(max_length=2000, blank=True, null=True)
    local_search_id = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "计算文件"
        verbose_name_plural = "计算文件"

    def __unicode__(self):
        return self.title


class SuiteTask(models.Model):
    """组计算任务"""
    sid = models.CharField(unique=True, blank=False, max_length=50,
                           verbose_name="id", primary_key=True,
                           default=get_sid)
    user = models.ForeignKey(UserProfile, blank=False, verbose_name="user")
    total_tasks = models.IntegerField(blank=False, verbose_name="total tasks")
    has_finished_tasks = models.IntegerField(blank=False, default=0,
                                             verbose_name="Finished number")
    start_time = models.DateTimeField(blank=False, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=2000, blank=True)
    notes = models.CharField(max_length=5000, blank=True)
    status = models.ForeignKey(StatusCategory, blank=False,
                               default=STATUS_UNDEFINED)
    models_str = models.CharField(max_length=2000, blank=True)
    models_category_str = models.CharField(max_length=200, blank=True)
    result_pdf = models.FileField(blank=True, null=True,
                                  upload_to=settings.PROCESS_FILE_PATH)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "组计算任务"
        verbose_name_plural = "组计算任务"

    def __unicode__(self):
        return self.sid


class SingleTask(models.Model):
    """单个计算任务"""
    sid = models.ForeignKey(SuiteTask, blank=False)
    pid = models.CharField(max_length=50, unique=True, blank=False,
                           primary_key=True, default=get_sid)
    temperature = models.FloatField(blank=True, default=-0.0)
    humidity = models.FloatField(blank=True, default=-0.0)
    other = models.FloatField(blank=True, default=-0.0)
    model = models.ForeignKey(ModelCategory, blank=False)
    results = models.TextField(blank=True, null=None)
    result_state = models.CharField(max_length=1000, blank=True, null=None)
    status = models.ForeignKey(StatusCategory, blank=False,
                               default=STATUS_WORKING)
    start_time = models.DateTimeField(blank=False, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    file_obj = models.ForeignKey(ProcessedFile, blank=False)
    result_pdf = models.FileField(blank=True, null=True,
                                  upload_to=settings.PROCESS_FILE_PATH)

    class Meta:
        verbose_name = "单个计算任务"
        verbose_name_plural = "单个计算任务"

    def __unicode__(self):
        return self.sid.name


class ChemInfoLocal(models.Model):
    """Chemistry database for locally search"""
    cas = models.CharField(max_length=200, blank=False, unique=True)
    einecs = models.CharField(max_length=2000, blank=False)
    einecs_name = models.CharField(max_length=2000, blank=False)
    einecs_mf = models.CharField(max_length=2000, blank=False)
    frequency = models.IntegerField(blank=False)
    positive_atoms = models.IntegerField(blank=False)
    negative_atoms = models.IntegerField(blank=False)
    formal_charge = models.IntegerField(blank=False)
    h_acceptors = models.IntegerField(blank=False)
    h_donors = models.IntegerField(blank=False)
    molecular_solubility = models.FloatField(blank=False)
    alogp = models.FloatField(blank=False)
    logd = models.FloatField(blank=False)
    molecular_formula = models.CharField(max_length=2000, blank=False)
    smiles = models.CharField(max_length=2000, blank=False)
    inchl = models.CharField(max_length=2000, blank=False)
    molecular_savol = models.FloatField(blank=False)
    image = models.FileField(upload_to=settings.SEARCH_IMAGE_PATH, blank=True)

    class Meta:
        verbose_name = "欧盟既有化学品数据库"
        verbose_name_plural = "欧盟既有化学品数据库"

    def __unicode__(self):
        return self.cas
