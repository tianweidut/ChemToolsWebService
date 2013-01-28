"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: main settings of Chemistry Tools Site
    Created: 2012-10-22
    Modified: 2012-12-11
"""

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


from django.contrib import admin

admin.autodiscover()

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    url(
        r'^$',
        direct_to_template, {'template': 'home/index.html'},
        name='index'
    ),
    url(
        r'^admin/',
        include(admin.site.urls),
        name="admin"
    ),
    url(
        r'^api/',
        include('api.urls'),
        name="api"
    ),
    url(
        r'^accounts/',
        include('registration.urls'),
        name="accounts"
    ),
    url(
        r'^download/$',
        direct_to_template, {'template': 'introduction/download.html'},
        name="download"
    ),
    url(
        r'^features/$',
        direct_to_template, {'template': 'introduction/features.html'},
        name="features"
    ),
    url(
        r'^info/$',
        direct_to_template, {'template': 'userprofile/navchart1.html'},
        name="info"
    ),
    url(
        r'^info/projects/$',
        direct_to_template, {'template': 'userprofile/navchart1.html'},
        name="info"
    ),
    url(
        r'^info/work_in_progress/$',
        direct_to_template, {'template': 'userprofile/navchart2.html'},
        name="info"
    ),
    url(
        r'^bootcamp/$',
        direct_to_template, {'template': 'features/bootcamp.html'},
        name="info"
    ),
    url(
        r'^newtask/$',
        direct_to_template, {'template': 'features/newtask.html'},
        name="newtask"
    ),
    url(
        r'^history/$',
        direct_to_template, {'template': 'features/history.html'},
        name="history"
    ),
    url(
        r'^search/$',
        direct_to_template, {'template': 'features/search.html'},
        name="search"
    ),
    url(
        r'^forum/',
        include('lbforum.urls'),
        name="forum"
    ),
    url(
        r'^attachments/', 
        include('attachments.urls'),
        name="attachments"
    ),

)


urlpatterns += patterns('', 
    url(
        r'^tags/$',
        direct_to_template, {'template':'home/index.html'},
        name="tags"
    ),
    url(
        r'^site_settings/$',
        direct_to_template, {'template':'home/index.html'},
        name="site_settings"
    ),
    url(
        r'^widgets/$',
        direct_to_template, {'template': 'home/index.html'},
        name="widgets"
    ),
    url(
        r'^about/$',
        direct_to_template, {'template': 'home/index.html'},
        name="about"
    ),
    url(
        r'^faq/$',
        direct_to_template, {'template': 'home/index.html'},
        name="faq"
    ),
    url(
        r'^help/$',
        direct_to_template, {'template': 'home/index.html'},
        name="help"
    ),
    url(
        r'^privacy/$',
        direct_to_template, {'template': 'home/index.html'},
        name="privacy"
    ),
    url(
        r'^users/$',
        direct_to_template, {'template': 'home/index.html'},
        name="users"
    ),
    url(
        r'^feedback/$',
        direct_to_template, {'template': 'home/index.html'},
        name="feedback"
    ),
    url(
        r'^questions/$',
        direct_to_template, {'template': 'home/index.html'},
        name="questions"
    ),
)

from fileupload.views import PictureCreateView,PictureDeleteView

urlpatterns += patterns('',
        url(r'^new/$', PictureCreateView.as_view(), {}, 'upload-new'),
        url(r'^delete/(?P<pk>\d+)$', PictureDeleteView.as_view(), {}, 'upload-delete'),)
