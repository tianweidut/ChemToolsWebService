# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''
from django.conf.urls.defaults import *
from piston.resource import Resource
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
        url(r'^/$' ,direct_to_template, {'template': 'userinfo/userinfo.html'}))
