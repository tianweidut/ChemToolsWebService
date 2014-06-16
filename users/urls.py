# coding: utf-8
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from users.views import (profile, admin_account,
                         active, register, api_login)


urlpatterns = patterns('',
    url(r'^settings/profile/$', profile, name="settings_profile"),
    url(r'^settings/admin/$', admin_account, name="settings_admin_account"),

    url(r'^api/login/$', api_login),

    url(r'^accounts/active/(?P<activation_key>\w+)/$', active,
        name='registration_avtive'),

    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^accounts/logout/$', auth_views.logout,
        {'template_name': 'index.html'},
        name='auth_logout'),

    url(r'^accounts/password/change/$', auth_views.password_change,
        name='auth_password_change'),
    url(r'^accounts/password/change/done/$', auth_views.password_change_done,
        name='auth_password_change_done'),
    url(r'^accounts/password/reset/$', auth_views.password_reset,
        name='auth_password_reset'),
    url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9a-zA-Z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='auth_password_reset_confirm'),
    url(r'^accounts/password/reset/complete/$', auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^accounts/password/reset/done/$', auth_views.password_reset_done,
        name='auth_password_reset_done'),

    url(r'accounts/register/$', register, name='registration_register'),
    url(r'accounts/register/complete/$',
        TemplateView.as_view(template_name='registration/registration_complete.html'),
        name='registration_complete'),
)
