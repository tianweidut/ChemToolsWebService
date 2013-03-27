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
from utils.ChemSpiderPy.wrapper import search_cheminfo
from backend.logging import logger
from fileupload.views import JSONResponse, response_minetype
from fileupload.models import ProcessedFile


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
    name = str(name)
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

    obj = ProcessedFile()
    obj.title = name + str(uuid.uuid4()) + "." + filetype
    wrapper_f.name = obj.title
    obj.file_obj = f
    obj.file_type = filetype if filetype != " " else "unknown"
    obj.save()

    return wrapper_f


def upload_response(request):
    """
        use AJAX to process file upload
    """
    wrapper_f = upload_save_process(request)
    path = settings.MEDIA_URL + settings.PROCESS_FILE_PATH
    data = [{'name': wrapper_f.name,
             'url': path + wrapper_f.name.replace(" ", "_"),
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
