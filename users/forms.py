# -*- coding: UTF-8 -*-
'''
Created on 2013-03-04

@author: tianwei

Desc: This module contains Forms for users.views.
'''

import logging

from django import forms
from django.db import models


class UserProfileForm(forms.Form):
    """
        UserProfile Form for /settings/profile
    """
    name = forms.CharField(
                    required=False,
                    max_length=255,
                    widget=forms.TextInput(attrs={"disabled":"disabled",
                                                  "class":"input-xlarge"}))

    email = forms.EmailField(
                    required=False,
                    max_length=255,
                    widget=forms.TextInput(attrs={"disabled":"disabled",
                                                  "class":"input-xlarge"}))

    telephone = forms.CharField(
                    required=False,
                    max_length=20,
                    widget=forms.TextInput(attrs={"class":"input-xlarge"}))

    company = forms.CharField(
                    required=False,
                    max_length=255,
                    widget=forms.TextInput(attrs={"class":"input-xlarge"}))

    location = forms.CharField(
                    required=False,
                    max_length=255,
                    widget=forms.TextInput(attrs={"class":"input-xlarge"}))

    machinecode = forms.CharField(
                            required=False,
                            max_length=100,
                            widget=forms.TextInput(attrs={"class":"input-xlarge"}))

    agentid = forms.CharField(
                            required=False,
                            max_length=100,
                            widget=forms.TextInput(attrs={"disabled":"disabled",
                                                          "class":"input-xlarge"}))

    def __init__(self, user, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["name"].initial = user.user.username
        self.fields["company"].initial = user.workunit
        self.fields["location"].initial = user.address
        self.fields["agentid"].initial = user.agentID
        self.fields["machinecode"].initial = user.machinecode
        self.fields["telephone"].initial = user.telephone
        self.fields["email"].initial = user.user.email

    def clean_name(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.name
        else:
            return self.cleaned_data.get("name", None)

    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.email
        else:
            return self.cleaned_data.get("email", None)

    def clean_agentid(self):
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.agentid
        else:
            return self.cleaned_data.get("agentid", None)
