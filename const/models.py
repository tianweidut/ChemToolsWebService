# coding: UTF-8
'''
Created on 2013-05-20

@author: tianwei

Desc: dict table
'''

from django.db import models

from const import * 

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


class ModelCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=MODEL_CHOICES,
                                verbose_name=u"Calculate Model")
    origin_type = models.ForeignKey(ModelTypeCategory, blank=False)
    desc = models.TextField(blank=True)

    class Meta:
        verbose_name = "Calculate Model"
        verbose_name_plural = "Calculate Model"

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
                                verbose_name=u"level bill")

    class meta:
        verbose_name = "level bill"
        verbose_name_plural = "levle bill"

    def __unicode__(self):
        return self.get_category_display()


class FileSourceCategory(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=MOL_ORIGIN_CHOICES,
                                default=ORIGIN_UNDEFINED)

    class meta:
        verbose_name = "file source"
        verbose_name_plural = "file source"

    def __unicode__(self):
        return self.get_category_display()
