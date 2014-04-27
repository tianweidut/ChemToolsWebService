#coding: utf-8

from django.contrib import admin
from users.models import (UserProfile, UserGrade,
                          RegistrationProfile, LevelAccountCategory,
                          LevelBillCategory, LevelGrageCategory)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'activation_key_expired')
    search_fileds = ('user__username', 'user__first_name')


UserClass = (UserProfile,
             UserGrade,
             RegistrationProfile,
             RegistrationAdmin,
             LevelAccountCategory,
             LevelBillCategory,
             LevelGrageCategory,
             )

for item in UserClass:
    admin.site.register(item)
