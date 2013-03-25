# -*- coding: UTF-8 -*-
'''
Created on 2013-01-20

@author: tianwei

Desc: Process File Model
'''

from django.db import models
from django.conf import settings


class Picture(models.Model):
    file = models.ImageField(upload_to="pictures")
    slug = models.SlugField(max_length=50, blank=True)

    def __unicode__(self):
        return self.file

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)


class ProcessedFile(models.Model):
    title = models.CharField(max_length=60, blank=False, unique=True)
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH+"/%Y/%m/%d")
    file_type = models.CharField(max_length=10, blank=False)

    def __unicode__(self):
        return self.title
