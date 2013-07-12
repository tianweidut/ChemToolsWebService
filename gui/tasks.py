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


def task_details_context(pid):
    """
    """
    singletask = get_object_or_404(SingleTask, pid=pid)

    try:
        search_engine = SearchEngineModel.objects.get(smiles__contains=singletask.file_obj.smiles)
    except Exception, err:
        loginfo(p=err)
        search_engine = None

    re_context = {"singletask": singletask,\
                  "search_engine": search_engine}

    return re_context


def get_ModelName(name):
    temp={
            "koa":"logKOA",
            "rp":"logRP",
            "koc":"logKOC",
            "bcf":"logBCF",
            }
    # return temp.get(name)
    if temp.has_key(name):
        return temp.get(name)
    else: 
        raise KeyError,"We don't have this model"


@task()
def add(x, y):
    print "sleep!"
    return x+y+x+y


@task()
def add_a(x, y):
    print "sleep! a"
    return x+y+x+y


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
    suite.save()


@task()
def add_counter(suite_id):
    """
    use filter to get task numbers
    """
    finished_count = SingleTask.objects.filter(sid=suite_id)\
                                       .exclude(status=StatusCategory.objects.get(category=STATUS_WORKING))\
                                       .count()
    print finished_count
    suite = SuiteTask.objects.get(sid=suite_id)
    if finished_count == suite.total_tasks:
        suite.has_finished_tasks = suite.total_tasks
        print "Finished:" + str(suite.has_finished_tasks)
        suite.status_id = StatusCategory.objects.get(category=STATUS_SUCCESS)
    else:
        suite.has_finished_tasks = finished_count

    suite.save()


@task()
def add_counter_cache(suite_id):
    """
    Add counter by cache
    """
    id = md5(suite_id).hexdigest()
    lock_id = "%s-lock-%s" % ("add_counter", id)

    # cache.add fails if if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    print cache.get(lock_id)

    if acquire_lock():
        print cache.get(lock_id)
        try:
            add_counter_core(suite_id)
        finally:
            release_lock()


@task()
def send_email(task):
    """
    send result email to user
    """
    pass


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


@task
def generate_pdf(id, task_type=None):
    """
    generate result in pdf format
    """
    if task_type == TASK_SINGLE:
        template = get_template("widgets/pdf/task_details_pdf.html")
    elif task_type == TASK_SUITE:
        template = get_template("widgets/pdf/suite_details_pdf.html")
    else:
        loginfo(p=task_type, label="Cannot check the type")
        return

    context = Context(task_details_context(pid=id))
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


def pdf_create_test():
    """
    pdf test create
    """
    task_id_search = "06b4c9a5-3a01-4bb4-a07c-d574d293d7e5"
    task_id_draw = "0a72a6ba-63f0-41db-a04f-f71c292f6db8"
    task_id_upload = "1142ae41-9497-4771-9c1c-d4dfcece994a"
    task_id_none = "16b4c9a5-3a01-4bb4-a07c-d574d293d7e5"

    print "search type for single task"
    generate_pdf(id=task_id_search, task_type=TASK_SINGLE)
    print "draw type for single task"
    generate_pdf(id=task_id_draw, task_type=TASK_SINGLE)
    print "upload type for single task"
    generate_pdf(id=task_id_upload, task_type=TASK_SINGLE)
    print "not found this task id"
    #generate_pdf(id=task_id_none, task_type=TASK_SINGLE)


def convert_smile_png(singletask):
    """
    convert mol into smile and png
    """
    abpath = singletask.file_obj.file_obj.url
    fullpath = settings.SETTINGS_ROOT + abpath

    print "convert_smile_png"
    mol = pybel.readfile("mol", fullpath).next()
    singletask.file_obj.smiles = ("%s" % mol).split("t")[0]

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
        singletask.file_obj.image = SearchEngineModel.objects.get(smiles__contains=singletask.file_obj.smiles).image
        singletask.file_obj.save()
        singletask.save()
    else:
        #other types only contains mol file
        print "other input method"
        convert_smile_png(singletask)


@task()
def calculateTask(task, model_name):
    """
    Calculate task
    """
    #Covert smiles, png
    generate_smile_image(task.pid)

    para = dict.fromkeys(['smilestring', 'filename', 'cas'], "")

    fullpath = os.path.join(settings.SETTINGS_ROOT, task.file_obj.file_obj.path)
    para['filename'] = os.path.basename(fullpath)
    filepath = os.path.dirname(fullpath)
    suite = task.sid
    result = 0

    print fullpath
    print para["filename"]
    print filepath

    try:
        pm = PredictionModel([get_ModelName(model_name)], para, filepath)
        result = pm.predict_results[para['filename'].split(".")[0]][get_ModelName(model_name)]
    except KeyError, err:
        print "We don't have this model"
        result = 0
        task.result_state = "We don't support this model now"
        task.status = StatusCategory.objects.get(category=STATUS_SUCCESS)
        suite.status_id = StatusCategory.objects.get(category=STATUS_WORKING)
    except Exception, err:
        print err
        result = -10000
        task.result_state = str(err)
        task.status = StatusCategory.objects.get(category=STATUS_FAILED)
        suite.status_id = StatusCategory.objects.get(category=STATUS_FAILED)
    else:
        print "calculate Successfully in celery queue!"
        task.result_state = "Calculate Successfully!"
        task.status = StatusCategory.objects.get(category=STATUS_SUCCESS)
        suite.status_id = StatusCategory.objects.get(category=STATUS_WORKING)
    suite.save()

    loginfo(p=result, label="calculate task result")
    task.end_time = datetime.datetime.now()
    task.results = result
    task.save()

    #Add single task counter
    add_counter.delay(suite.sid)

    return result
