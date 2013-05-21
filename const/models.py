# coding: UTF-8
'''
Created on 2013-05-20

@author: tianwei

Desc: dict table
'''

from django.db import models

from const import FILE_CHOICES
from const import MODEL_CHOICES, MODEL_ORIGIN_CHOICES
from const import LEVEL_CHOICES, LEVEL2_CHOICES, LEVEL3_CHOICES
from const import STATUS_CHOICES


class PresentationCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=FILE_CHOICES,
                                verbose_name=u"Attachment File Type")

    class Meta:
        verbose_name = "Attachment File Types"
        verbose_name_plural = "Attachment File Types"

    def __unicode__(self):
        return self.get_category_display()


class ModelCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=MODEL_CHOICES,
                                verbose_name=u"Calculate Model")
    origin_type = models.ForeignKey(ModelTypeCategory, blank=False)

    class Meta:
        verbose_name = "Calculate Model"
        verbose_name_plural = "Calculate Model"

    def __unicode__(self):
        return self.get_category_display()


class ModelTypeCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=MODEL_ORIGIN_CHOICES,
                                verbose_name=u"Calculate Model Type")

    class Meta:
        verbose_name = "Calculate Model Type"
        verbose_name_plural = "Calculate Model Type"

    def __unicode__(self):
        return self.get_category_display()


class StatusCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=STATUS_CHOICES,
                                verbose_name=u"calculate status")

    class Meta:
        verbose_name = "Calculate Status"
        verbose_name_plural = "Calculate Status"

    def __unicode__(self):
        return self.get_category_display()


class LevelGrageCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=LEVEL2_CHOICES,
                                verbose_name=u"Level grade")

    class Meta:
        verbose_name = "Level grage"
        verbose_name_plural = "Levle grade"

    def __unicode__(self):
        return self.get_category_display()


class LevelAccountCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=LEVEL_CHOICES,
                                verbose_name=u"Level account")

    class Meta:
        verbose_name = "Level account"
        verbose_name_plural = "Levle account"

    def __unicode__(self):
        return self.get_category_display()


class LevelBillCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=LEVEL3_CHOICES,
                                verbose_name=u"Level bill")

    class Meta:
        verbose_name = "Level bill"
        verbose_name_plural = "Levle bill"

    def __unicode__(self):
        return self.get_category_display()
