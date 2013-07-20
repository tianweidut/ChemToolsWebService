# coding: UTF-8
'''
Created on 2013-04-06

@author: tianwei

Desc: Celery Tasks
'''
import os
import sys
import uuid
import time
import datetime

from celery.decorators import task

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.utils import simplejson
from django.core.files import File
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor as md5
from django.template.loader import get_template
from django.template import Context

#import ho.pisa as pisa
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO

from calcore.controllers.prediciton_model import PredictionModel
from backend.logging import logger, loginfo
from calcore.models import SingleTask, ProcessedFile, SuiteTask
from const.models import StatusCategory
from const import STATUS_WORKING, STATUS_SUCCESS, STATUS_FAILED, STATUS_UNDEFINED

import pybel
from calcore.models import *
from const import ORIGIN_DRAW, TASK_SUITE, TASK_SINGLE


LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes


def suite_details_context(sid):
    """
    """
    suitetask = get_object_or_404(SuiteTask, sid=sid)

    suitetask = get_object_or_404(SuiteTask, sid=sid)
    single_lists = SingleTask.objects.filter(sid=sid)

    re_context = {"suitetask": suitetask,
                  "single_lists": single_lists}

    return re_context


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


def fetch_resources(uri, rel):
    """
    change pisa resource url to retrive
    pictures, css etc.
    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))

        if not os.path.isfile(path):
            path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

            if not os.path.isfile(path):
                raise Exception("Cannot import MEDIA_ROOT or STATIC_ROOT")

    return path


def generate_pdf(id, task_type=None):
    """
    generate result in pdf format
    Output:
        file full path
    """
    if task_type == TASK_SINGLE:
        template = get_template("widgets/pdf/task_details_pdf.html")
        context = Context(task_details_context(pid=id))
    elif task_type == TASK_SUITE:
        template = get_template("widgets/pdf/suite_details_pdf.html")
        context = Context(suite_details_context(sid=id))
    else:
        loginfo(p=task_type, label="Cannot check the type")
        return

    html = template.render(context).encode("UTF-8")
    html = StringIO.StringIO(html)

    try:
        name = str(uuid.uuid4()) + ".pdf"
        path = os.path.join(settings.SEARCH_IMAGE_PATH, name)
        f = open(path, "w")
        pisa.CreatePDF(html, dest=f, encoding="UTF-8",
                       link_callback=fetch_resources)
        f.close()
        print "finish pdf generate"
    except Exception, err:
        loginfo(p=err, label="cannot generate pdf")

    return path


def pdf_create_test():
    """
    pdf test create
    """
    task_id_search = "06b4c9a5-3a01-4bb4-a07c-d574d293d7e5"
    task_id_draw = "0a72a6ba-63f0-41db-a04f-f71c292f6db8"
    task_id_upload = "1142ae41-9497-4771-9c1c-d4dfcece994a"
    task_id_none = "16b4c9a5-3a01-4bb4-a07c-d574d293d7e5"
    task_id_ch = "17673ac1-17dd-4f0d-958a-4ef44bba8a92"
    suite_id = "c933deb5-beda-4a41-84be-759a5795aca1"

    print "search type for single task"
    generate_pdf(id=task_id_search, task_type=TASK_SINGLE)
    print "draw type for single task"
    generate_pdf(id=task_id_draw, task_type=TASK_SINGLE)
    print "upload type for single task"
    generate_pdf(id=task_id_upload, task_type=TASK_SINGLE)
    print "not found this task id"
    #generate_pdf(id=task_id_none, task_type=TASK_SINGLE)
    generate_pdf(id=task_id_ch, task_type=TASK_SINGLE)
    print "suite task id"
    generate_pdf(id=suite_id, task_type=TASK_SUITE)


def convert_smile_png(singletask):
    """
    convert mol into smile and png
    """
    abpath = singletask.file_obj.file_obj.url
    fullpath = settings.SETTINGS_ROOT + abpath

    print "convert_smile_png"
    mol = pybel.readfile("mol", fullpath).next()
    singletask.file_obj.smiles = ("%s" % mol).split("\t")[0]

    picname = str(uuid.uuid4()) + ".png"
    picpath = os.path.join(settings.SEARCH_IMAGE_PATH, picname)
    mol.draw(show=False, filename=picpath)

    f = File(open(picpath, "r"))
    singletask.file_obj.image = f
    singletask.file_obj.save()
    singletask.save()
    f.close()
    print singletask.file_obj.smiles
    print singletask.file_obj.image


def generate_smile_image(pid):
    """
    generate smile and image for task
    """
    singletask = SingleTask.objects.get(pid=pid)
    filetype = singletask.file_obj.file_source.category

    if filetype == ORIGIN_SMILE:
        #this type has already have image and smiles in local search machine,
        #only copy them
        print "search engine test"
        print singletask.file_obj.smiles
        print SearchEngineModel.objects.get(smiles=singletask.file_obj.smiles).image
        singletask.file_obj.image = SearchEngineModel.objects.get(smiles=singletask.file_obj.smiles).image
        singletask.file_obj.save()
        singletask.save()
    else:
        #other types only contains mol file
        print "other input method"
        convert_smile_png(singletask)


def add_counter_core(suite_id):
    """
    core counter algorightm
    """
    print "add counter"
    suite = SuiteTask.objects.get(sid=suite_id)
    if suite.has_finished_tasks < suite.total_tasks-1:
        suite.has_finished_tasks = suite.has_finished_tasks + 1
        print "add:" + str(suite.has_finished_tasks)
    else:
        suite.has_finished_tasks = suite.total_tasks
        print "Finished:" + str(suite.has_finished_tasks)
        print suite.has_finished_tasks
        suite.status_id = StatusCategory.objects.get(category=STATUS_SUCCESS)
        # generate suite task report and send email
        
       # try:
       #     file_path = generate_pdf(id=suite_id, task_type=TASK_SUITE)
       #     f = File(open(file_path, "r"))
       #     suite.result_pdf = f
       #     f.close()
#except Exception, err:
 #           loginfo(p=err, label="generate pdf error!")

    suite.save()
