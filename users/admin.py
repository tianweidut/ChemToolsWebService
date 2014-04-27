#coding: utf-8

from django.contrib import admin
from users.models import (UserProfile, UserGrade,
                          RegistrationProfile, LevelAccountCategory,
                          LevelBillCategory, LevelGrageCategory)

UserClass = (UserProfile,
             UserGrade,
             RegistrationProfile,
             LevelAccountCategory,
             LevelBillCategory,
             LevelGrageCategory,
             )

for item in UserClass:
    admin.site.register(item)
