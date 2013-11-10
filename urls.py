#coding: utf-8
"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: main settings of Chemistry Tools Site
    Created: 2012-10-22
    Modified: 2013-05-13
"""

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()
admin.autodiscover()

handler500 = 'backend.errorviews.error500'
handler403 = 'backend.errorviews.error403'
handler404 = 'backend.errorviews.error404'

urlpatterns = patterns('',
    url(
        r'^$',
        direct_to_template, {'template': 'home/index.html'},
        name='index'
    ),
    url(
        r'^admin/',
        include(admin.site.urls),
    ),
    url(
        r'^api/',
        include('api.urls'),
    ),
    url(
        r'^settings/',
        include('users.urls'),
    ),
    url(
        r'^accounts/',
        include('registration.urls'),
        name="accounts"
    ),
    url(
        '^download/$',
        direct_to_template, {'template': 'introduction/download.html'},
        name="download"
    ),
    url(
        r'^features/$',
        direct_to_template, {'template': 'introduction/features.html'},
        name="features"
    ),
    url(
        r'',
        include('gui.urls'),
    ),
    url(
        dajaxice_config.dajaxice_url,
        include('dajaxice.urls')
    ),
)

urlpatterns += staticfiles_urlpatterns()

# for develop to serve user-upload content in MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'media/(?P<path>.*)$',
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
                )
