# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from users.views import (profile, admin_account, billing, payments,
                         active, register, api_login)


urlpatterns = patterns('',
    url(r'^profile/$', profile, name="settings_profile"),
    url(r'^admin/$', admin_account, name="settings_admin_account"),
    url(r'^billing/$', billing, name="settings_billing"),
    url(r'^payments/$', payments, name="settings_payments"),
    url(r'^active/(?P<activation_key>\w+)/$', active,
        name='registration_avtive'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^api/login/$', api_login)
    url(r'^logout/$', auth_views.logout, {'template_name': 'home/index.html'},
        name='auth_logout'),
    url(r'^password/change/$', auth_views.password_change,
        name='auth_password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9a-zA-Z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'register/$', register, name='registration_register'),
    url(r'register/complete/$',
        TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),
)
