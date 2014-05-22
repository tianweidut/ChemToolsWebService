#coding: utf-8
from django.conf.urls import patterns, url
from chemistry import views, api_views
from django.views.generic import TemplateView


urlpatterns = patterns('',
    #url(r'^newtask/$', views.submit),
    url(r'^newtask/$', TemplateView.as_view(template_name='newtask.html')),
    url(r'^history/$', views.history),
    url(r'^details/suite/(?P<sid>.{36})$', views.suitetask),
    url(r'^details/task/(?P<pid>.{36})$', views.singletask),

    url(r'^api/smile-search/$', api_views.smile_search),
    url(r'^api/mol-upload/$', api_views.mol_upload),
    url(r'^api/task-submit/$', api_views.task_submit),
    url(r'^api/suitetask/$', api_views.suitetask),
    url(r'^api/singletask/$', api_views.singletask),
    url(r'^api/history/$', api_views.history),
)
