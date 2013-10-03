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
        gui_views.history_view,
        name="history"
    ),
    url(
        r'^details/suite/(?P<sid>.{36})$',
        gui_views.suite_details_view,
        name="suite_details"
    ),
    url(
        r'^details/task/(?P<pid>.{36})$',
        gui_views.task_details_view,
        name="task_details"
    ),
    url(
        r'^settings/profile/$',
        users_views.profile,
        name="settings_profile"
    ),
    url(
        r'^settings/admin/$',
        users_views.admin_account
    ),
    url(
        r'^settings/billing/$',
        users_views.billing,
        name="settings_billing"
    ),
    url(
        r'^settings/payments/$',
        users_views.payments,
        name="settings_payments"
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
