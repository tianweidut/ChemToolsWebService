#coding: utf-8
from django.conf.urls import patterns, url

from .views import (submit, history, suitetask, singletask)


urlpatterns = patterns('',
    url(r'^newtask/$', submit),
    url(r'^history/$', history),
    url(r'^details/suite/(?P<sid>.{36})$', suitetask),
    url(r'^details/task/(?P<pid>.{36})$', singletask),
)
