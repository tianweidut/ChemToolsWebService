# -*- coding: UTF-8 -*-
'''
Created on 2013-03-03

@author: tianwei

Desc: This module contains views that allow users to submit the calculated
      tasks.
'''
import datetime
import logging
import os
import sys

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required

from gui import forms
from utils.ChemSpiderPy.wrapper import search_cheminfo
from backend.logging import logger


def step1_form(request):
    """
        Step1 for module choice,
        basic info input and search
    """
    data = {}
    search_result = None
    if request.method == "POST":
        basic_form = forms.BasicInfoForm(request.POST)

        if basic_form.is_valid():
            search_text = basic_form.cleaned_data["info"]
            search_result = search_cheminfo(search_text)
            data = {"is_valid": True,
                    "is_searched": True,
                    "search_result": search_result,
                    "basic_form": basic_form}
        else:
            data = {"is_valid": False,
                    "is_searched": True,
                    "search_result": "None",
                    "basic_form": basic_form}
        return data
    else:
        basic_form = forms.BasicInfoForm()
        data = {"is_valid": True,
                "is_searched": False,
                "search_result": "None",
                "basic_form": basic_form}

        return data


def step2_form(request):
    """
        Step2 for module choice,
        choice chemistry models
    """
    pass


def step3_form(request):
    """
        Step3 for module choice,
        response message
    """
    pass

def step4_form(request):
    """
        Step4 for module choice,
        show all submit information, which will contain error message
    """
    pass


@login_required
def basic_search(request):
    """
        basic info search view function
        for STEP1 page and Search page
    """
    step1_data = {}
    step2_data = {}
    step3_data = {}

    if request.method == "POST":
        step1_data = step1_form(request)
        step2_data = step2_form(request)
        step3_data = step3_form(request)
    else:
        step1_data = step1_form()
        step2_data = step2_form()
        step3_data = step3_form()

    data = dict(step1_data, **dict(step2_data, **step3_data))
    return render(request, "features/newtask.html", data)
