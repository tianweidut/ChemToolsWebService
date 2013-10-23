#coding: utf-8
from django.conf.urls import patterns, url
from .views import (profile, admin_account, billing, payments)

urlpatterns = patterns('',
    url(r'^profile/$',
        profile,
        name="settings_profile"
        ),
    url(r'^admin/$',
        admin_account,
        name="settings_admin_account"
        ),
    url(r'^billing/$',
        billing,
        name="settings_billing"
        ),
    url(
        r'^payments/$',
        payments,
        name="settings_payments"
        )
)
