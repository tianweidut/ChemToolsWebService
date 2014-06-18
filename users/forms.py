# coding: utf-8
from django import forms
from django.forms.util import ErrorList
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from users.models import RegistrationProfile

from utils import loginfo


attrs_dict = {'class': 'required'}


class UserProfileForm(forms.Form):
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
        password = self.cleaned_data.get("old_password", "").strip()
        new_password = self.cleaned_data.get("new_password", "").strip()
        new_password2 = self.cleaned_data.get("new_password2", "").strip()

        # check password from database
        user = authenticate(username=self.user.user.username,
                            password=password)

        if user is None:
            self._errors["old_password"] = ErrorList(
                [u'Please input the corrected password!'])
            if self.cleaned_data.get("old_password", None) is not None:
                del self.cleaned_data["old_password"]

        # check newpassword twice
        if new_password != new_password2:
            self._errors["new_password2"] = ErrorList([u'The twiced password\
                cannot match!'])
            if self.cleaned_data.get("new_password2", None) is not None:
                del self.cleaned_data["new_password2"]

        return self.cleaned_data


class RegistrationForm(forms.Form):
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                label=_(u'username'),
                                widget=forms.TextInput(
                                    attrs={'placeholder': _(u'username'),
                                           "class": "required"}))

    email = forms.EmailField(label=_(u'email address'),
                             widget=forms.TextInput(
                                 attrs={'placeholder': _(u'email address'),
                                        "class": "required"}))

    password1 = forms.CharField(label=_(u'password'),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': _(u'password'),
                                           "class": "required"},
                                    render_value=False))

    password2 = forms.CharField(label=_(u'password (again)'),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': _(u'password(again)'),
                                           "class": "required"},
                                    render_value=False))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(
                    _(u'You must type the same password each time!'))
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
            loginfo(p=user, label="user")
            loginfo(p=self.cleaned_data["username"], label="text")
        except User.DoesNotExist:
            return self.cleaned_data

        raise forms.ValidationError(
            _(u'This username is already taken. Please choose another.'))

    def save(self, request, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(
                        request,
                        username=self.cleaned_data['username'],
                        email=self.cleaned_data['email'],
                        password=self.cleaned_data['password1'],
                        profile_callback=profile_callback)

        return new_user


class RegistrationFormTermsOfService(RegistrationForm):
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'))

    def clean_tos(self):
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(
            _(u'You must agree to the terms to register'))


class RegistrationFormUniqueEmail(RegistrationForm):
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _(u'This email address is already in use. Please supply a different email address.'))
        return self.cleaned_data['email']
