# -*- coding: UTF-8 -*-
'''
Created on 2013-03-03

@author: tianwei

Desc: This module contains Forms for gui.views.
'''

import logging

from django import forms
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms.util import ErrorList


class BasicInfoForm(forms.Form):
    """
        Basic search input-text
    """
    info = forms.CharField(help_text="Input cas, name, smiles, search you want",
                           required=False,
                           max_length=255,
                           widget=forms.TextInput(attrs={'placeholder': 'cas,name,smiles...',
                                                         'class': "span4 search-query"}),)

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)


class ResponseMessageForm(forms.Form):
    """
        Response message form
    """
    txt_choice = forms.BooleanField(widget=forms.CheckboxInput())
    pdf_choice = forms.BooleanField(widget=forms.CheckboxInput())
    csv_choice = forms.BooleanField(widget=forms.CheckboxInput())
    commit_notes = forms.CharField(help_text="input some comments for check list",
                                   required=False,
                                   max_length=1000,
                                   widget=forms.TextInput(attrs={'placeholder': 'some comments',
                                                                 "class": ""}))
    name = forms.CharField(help_text="name for this task",
                           required=True,
                           max_length=255,
                           widget=forms.TextInput(attrs={'placeholder': 'some comments',
                                                         "class": ""}))

    def __init__(self, *args, **kwargs):
        super(ResponseMessageForm, self).__init__(*args, **kwargs)
    
    def cleaned_name(self):
        """
            unique name check
        """
        pass
