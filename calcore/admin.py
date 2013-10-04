# coding: UTF-8
'''
Created on 2012-11-5

@author: tianwei
'''

from django.contrib import admin
from calcore.models import (SuiteTask, SingleTask, ProcessedFile,
                            SearchEngineModel, ChemInfoLocal)


RegisterClass = (SuiteTask,
                 SingleTask,
                 ProcessedFile,
                 SearchEngineModel,
                 ChemInfoLocal,
                 )

for item in RegisterClass:
    admin.site.register(item)
