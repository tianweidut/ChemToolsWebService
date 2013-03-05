# -*- coding: UTF-8 -*-
'''
Created on 2013-03-04

@author: tianwei

Desc: This module contains Forms for users.views.
'''

import logging

from django import forms
from django.db import models
from django.forms.util import ErrorList
from django.contrib.auth import authenticate


class UserProfileForm(forms.Form):
    """
        UserProfile Form for /settings/profile
    """
    name = forms.CharField(required=False,
                           max_length=255,
                           widget=forms.TextInput(attrs={"disabled": "disabled",
                                                         "class": "input-xlarge"}))

    email = forms.EmailField(required=False,
                             max_length=255,
                             widget=forms.TextInput(attrs={"disabled": "disabled",
                                                           "class": "input-xlarge"}))

    telephone = forms.CharField(required=False,
                                max_length=20,
                                widget=forms.TextInput(attrs={"class": "input-xlarge"}))

    company = forms.CharField(required=False,
                              max_length=255,
                              widget=forms.TextInput(attrs={"class": "input-xlarge"}))

    location = forms.CharField(required=False,
                               max_length=255,
                               widget=forms.TextInput(attrs={"class": "input-xlarge"}))

    machinecode = forms.CharField(required=False,
                                  max_length=100,
                                  widget=forms.TextInput(attrs={"class": "input-xlarge"}))

    agentid = forms.CharField(required=False,
                              max_length=100,
                              widget=forms.TextInput(attrs={"disabled": "disabled",
                                                            "class": "input-xlarge"}))

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

class PasswordForm(forms.Form):
    """
        User change password form
    """
    old_password = forms.CharField(required=True,
                                   max_length=255,
                                   widget=forms.PasswordInput(attrs={"class": "input-xlarge"}))
    new_password = forms.CharField(required=True,
                                   min_length=6,
                                   max_length=255,
                                   widget=forms.PasswordInput(attrs={"class": "input-xlarge"}))
    new_password2 = forms.CharField(required=True,
                                    min_length=6,
                                    max_length=255,
                                    widget=forms.PasswordInput(attrs={"class": "input-xlarge"}))
    user = None

    def __init__(self, user, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        """
            self clean form data
        """
        password = self.cleaned_data.get("old_password", "").strip()
        new_password = self.cleaned_data.get("new_password", "").strip()
        new_password2 = self.cleaned_data.get("new_password2", "").strip()

        # check password from database
        user = authenticate(username=self.user.user.username,
                            password=password)

        if user is None:
            self._errors["old_password"] = ErrorList([u'Please input the corrected password!'])
            if self.cleaned_data.get("old_password", None) is not None:
                del self.cleaned_data["old_password"]

        # check newpassword twice
        if new_password != new_password2:
            self._errors["new_password2"] = ErrorList([u'The twiced password\
                cannot match!'])
            if self.cleaned_data.get("new_password2", None) is not None:
                del self.cleaned_data["new_password2"]

        return self.cleaned_data
