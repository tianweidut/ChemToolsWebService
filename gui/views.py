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
import uuid

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
from django.core.files.uploadedfile import UploadedFile

from gui import forms
from backend.fileoperator import receiveFile
from backend.ChemSpiderPy.wrapper import search_cheminfo
from backend.logging import logger
from backend.utilities import JSONResponse, response_minetype
#from calcore.models import ProcessedFileedFile
from calcore.models import *


def step1_form(request=None):
    """
        Step1 for module choice,
        basic info input and search
    """
    data = {}
    search_result = None
    if request is not None:
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


def split_name(name, sep="."):
    """
        split type and name in a filename
    """
    if sep in name:
        f = name.split(sep)[0]
        t = name.split(sep)[1]
    else:
        f = name
        t = " "

    return (f, t)


def upload_save_process(request):
    """
        save file into local storage
    """
    f = request.FILES["file"]
    wrapper_f = UploadedFile(f)

    name, filetype = split_name(wrapper_f.name)
    #TODO: we maybe check file type here!

    obj = ProcessedFile()
    obj.title = name
    obj.file_type = filetype
    obj.file_obj = f
    obj.save()

    return obj


def upload_response(request):
    """
        use AJAX to process file upload
    """
    f = upload_save_process(request)
    data = [{'name': f.title,
             'id': f.fid,
             'type': f.file_type,
             }]

    response = JSONResponse(data, {}, response_minetype(request))
    response["Content-Dispostion"] = "inline; filename=files.json"

    return response


@login_required
def multi_inputform(request):
    """
    Multi input form:
       * basic info search view function
         for STEP1 page and Search page
       * multi files upload
    """
    if request.method == "POST":
        if request.FILES is not None:
            return upload_response(request)

    return render(request, "features/newtask.html")

def task_list(request):
    #SuiteTask_list = SuiteTask.objects.get(user=request.user.username)
    SuiteTask_list = SuiteTask.objects.all()
    return render(request, 'features/history.html', {'SuiteTask_list':SuiteTask_list})
