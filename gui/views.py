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
from backend.utilities import *
from calcore.models import *
from const import MODEL_SPLITS
from const import ORIGIN_UPLOAD


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


@login_required
def history_view(request):
    """
    """
    result_sets = SuiteTask.objects.filter(user__user=request.user).order_by('-start_time')

    #Add more attributes inito SuiteTask_list
    for task in result_sets:
        task.models_str_list = get_models_selector(task.models_str)
        task.models_category_str_list = get_models_selector(task.models_category_str)
        task.progress_value = "%0.2f"%(float(task.has_finished_tasks) / task.total_tasks * 100)
        task.is_finished = True if task.total_tasks == task.has_finished_tasks else False

    return render(request, 'features/history.html',
                  {'history_lists': result_sets})


#TODO: Add only user decorators
@login_required
def suite_details_view(request, sid=None):
    """
    Suitetask details view
    """
    suitetask = get_object_or_404(SuiteTask, sid=sid)
    single_lists = SingleTask.objects.filter(sid=sid)

    return render(request, 'features/details.html',
                  {"suitetask": suitetask,
                   "single_lists": single_lists})


def task_details_context(pid):
    """
    """
    singletask = get_object_or_404(SingleTask, pid=pid)

    try:
        search_engine = SearchEngineModel.objects.get(smiles=singletask.file_obj.smiles)
    except Exception, err:
        loginfo(p=err)
        search_engine = None

    re_context = {"singletask": singletask,\
                  "search_engine": search_engine}

    return re_context


#TODO: Add only user decorators
@login_required
def task_details_view(request, pid=None):
    """
    Every singletask details view
    """
    re_context = task_details_context(pid)

    return render(request, 'widgets/task_details.html', re_context)
