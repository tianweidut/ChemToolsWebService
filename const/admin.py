# coding: UTF-8
'''
Created on 2012-11-5

@author: tianwei
'''

from django.contrib import admin
from const.models import *


RegisterClass = (PresentationCategory,
                 ModelCategory,
                 ModelTypeCategory,
                 StatusCategory,
                 LevelAccountCategory,
                 LevelBillCategory,
                 LevelGrageCategory,
                 )

for item in RegisterClass:
    admin.site.register(item)
