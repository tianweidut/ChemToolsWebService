# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''

from django.contrib import admin
from gui.models import *

RegisterClass =(
                ActiveKeyInfo,
                ActiveHistory,
                ModelInfo,
                CompoundInfo,
                CompoundName,
                CalculateHistory,
                LanguageEnum,
                )

for item in RegisterClass:
    admin.site.register(item)


