# coding: utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView

admin.autodiscover()

handler500 = 'utils.error_views.error500'
handler403 = 'utils.error_views.error403'
handler404 = 'utils.error_views.error404'

urlpatterns = patterns('',
                       url(
                           r'^$',
                           TemplateView.as_view(template_name='home/index.html'),
                           name='index'
                       ),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('users.urls')),
                       url(r'', include('chemistry.urls')),
                       url(
                           '^download/$',
                           TemplateView.as_view(template_name='introduction/download.html'),
                           name="download"
                       ),
                       url(
                           r'^features/$',
                           TemplateView.as_view(template_name='introduction/features.html'),
                           name="features"
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
