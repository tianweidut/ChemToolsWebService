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

from gui import views as gui_views
from users import views as users_views


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
        r'^info/$',
        direct_to_template, {'template': 'features/userprofile.html'},
        name="info"
    ),
    url(
        r'^bootcamp/$',
        direct_to_template, {'template': 'features/bootcamp.html'},
        name="info"
    ),
    url(
        r'^newtask/$',
        gui_views.multi_inputform
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
