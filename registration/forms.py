# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''
#Forms and validation code for user registration.
import uuid

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from registration.models import RegistrationProfile

attrs_dict = {'class':'required'}

class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    """
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                label=_(u'username'),
                                widget=forms.TextInput(
                                    attrs={'placeholder':_(u'username'),
                                        "class":"required"}))

    email = forms.EmailField(label=_(u'email address'),
                             widget=forms.TextInput(
                                 attrs={'placeholder':_(u'email address'),
                                        "class":"required"}))

    password1 = forms.CharField(label=_(u'password'),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder':_(u'password'),
                                        "class":"required"},
                                    render_value=False))

    password2 = forms.CharField(label=_(u'password (again)'),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder':_(u'password(again)'),
                                        "class":"required"},
                                    render_value=False))
    
    machinecode = forms.RegexField(regex=r'^\w+$',
                                max_length=60,
                                label=_(u'machine code'),
                                widget=forms.TextInput(
                                    attrs={'placeholder':_(u'machinecode'),
                                        "class":"required"}))

    def clear_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    def clean(self):
        """
         Verifiy that the values entered into the two password fields match
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data

    def save(self, request, profile_callback=None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        """
        new_user = RegistrationProfile.objects.create_inactive_user(request,
                                                                    username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    machinecode=self.cleaned_data['machinecode'],
                                                                    profile_callback=profile_callback)

        return new_user


class RegistrationFormTermsOfService(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.    
    """
    tos = forms.BooleanField(widget = forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'))

    def clean_tos(self):
        """
        Validate that the user accepted the Terms of Service.        
        """
        if self.cleaned_data.get('tos',False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(_(u'You must agree to the terms to register'))        


class RegistrationFormUniqueEmail(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    email addresses.    
    """
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email'] 
