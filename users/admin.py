#coding: utf-8

from django.contrib import admin
from users.models import UserProfile, RegistrationProfile

UserClass = (UserProfile,
             RegistrationProfile,
             )

for item in UserClass:
    admin.site.register(item)
