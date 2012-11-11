# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''
from django.contrib import admin
from registration.models import RegistrationProfile

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'activation_key_expired')
    search_fileds = ('user__username', 'user__first_name')
    
admin.site.register(RegistrationProfile, RegistrationAdmin)
