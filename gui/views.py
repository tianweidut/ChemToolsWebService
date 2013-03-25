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
from django.core.files.uploadedfile import UploadedFile

from gui import forms
from backend.fileoperator import receiveFile
from utils.ChemSpiderPy.wrapper import search_cheminfo
from backend.logging import logger
from fileupload.views import JSONResponse, response_minetype
from fileupload.models import Image


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


@login_required
def multi_inputform(request):
    """
    Multi input form:
       * basic info search view function
         for STEP1 page and Search page
       * multi files upload 
    """
    step1_data = {}

    if request.method == "POST":
        file_obj = request.FILES
        if file_obj is None:
            step1_data = step1_form(request)
        else:
            f = file_obj["file"]
            saved_file = UploadedFile(file_obj["file"])
            
            image = Image()
            image.title = str(saved_file.name)
            image.image = f
            image.save()
            

            path = settings.MEDIA_URL + "tmp/"
            upload_data = [{'name':saved_file.name,
                            'url': path + saved_file.name.replace(" ", "_"),
                            }]
            response = JSONResponse(upload_data, {}, response_minetype(request))  
            response["Content-Dispostion"] = "inline; filename=files.json"
            
            return response
    else:
        step1_data = step1_form()

    data = dict(step1_data)
    return render(request, "features/newtask.html", data)
