from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

import settings


from django.contrib import admin
admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(r'^$',direct_to_template, {'template':'index.html'},"home"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include('api.urls')),
    
    url(r'^accounts/',include('registration.urls')),
    url(r'^download/$',direct_to_template,{'template':'introduction/download.html'}),
    url(r'^features/$',direct_to_template,{'template':'introduction/features.html'}),

    url(r'^forum/',include('lbforum.urls')),
    url(r'^attachments/', include('attachments.urls')),

)


