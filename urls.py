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

from gui import views as gui_views
from users import views as users_views


admin.autodiscover()
dajaxice_autodiscover()

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
        r'^newtask/$',
        gui_views.multi_inputform,
        name="newtasks"
    ),
    url(
        r'^history/$',
        gui_views.task_list,
        #direct_to_template, {'template': 'features/history.html'},
       # name="history"
    ),
    url(
        r'^details/$',
        direct_to_template, {'template': 'features/details.html'},
        name="details"
    ),
    url(
        r'^settings/profile/$',
        users_views.profile
    ),
    url(
        r'^settings/admin/$',
        users_views.admin_account
    ),
    url(
        r'^settings/billing/$',
        users_views.billing
    ),
    url(
        r'^settings/payments/$',
        users_views.payments
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
