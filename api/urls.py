#coding: utf-8
from django.conf.urls.defaults import patterns, url

from .views import (login, smile_search, mol_upload,
                    task_submit, suitetask, singletask,
                    history)

urlpatterns = patterns('',
    url(r'^login/$', login),
    url(r'^smile-search/$', smile_search),
    url(r'^mol-upload/$', mol_upload),
    url(r'^task-submit/$', task_submit),
    url(r'^suitetask/$', suitetask),
    url(r'^singletask/$', singletask),
    url(r'^history/$', history),
)
