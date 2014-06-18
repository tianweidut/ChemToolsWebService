# coding: UTF-8
from django.contrib import admin
from chemistry.models import (ModelCategory,
                              ModelTypeCategory, StatusCategory,
                              FileSourceCategory, SuiteTask, SingleTask,
                              ProcessedFile, SearchEngineModel, ChemInfoLocal)

RegisterClass = (
                 ModelCategory,
                 ModelTypeCategory,
                 StatusCategory,
                 FileSourceCategory,
                 SuiteTask,
                 SingleTask,
                 ProcessedFile,
                 SearchEngineModel,
                 ChemInfoLocal,
                 )

for item in RegisterClass:
    admin.site.register(item)
