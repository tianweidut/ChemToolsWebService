
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
    info = forms.CharField(
            help_text="Input cas, name, smiles, search you want",
            required=False,
            max_length=255,
            widget=forms.TextInput(attrs={'placeholder': 'cas,name,smiles...',
                                          'class': "span4 search-query"}),)

    def __init__(self, *args, **kwargs):
        super(BasicInfoForm, self).__init__(*args, **kwargs)
