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
from django.http import HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.core.files import File
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor as md5
from calcore.controllers.prediciton_model import PredictionModel
from backend.logging import logger, loginfo
from calcore.models import SingleTask, ProcessedFile, SuiteTask
from const.models import StatusCategory
from const import STATUS_WORKING, STATUS_SUCCESS, STATUS_FAILED, STATUS_UNDEFINED

import pybel
from calcore.models import *
from const import ORIGIN_DRAW


LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes


def get_ModelName(name):
    temp={
            "koa":"logKOA",
            "pl":"logRP",
            "kof":"logKOF"
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


@task
def generate_pdf(task):
    """
    generate result in pdf format
    """
    pass


def convert_smile_png(singletask):
    """
    convert mol into smile and png
    """
    abpath = singletask.file_obj.file_obj.url
    fullpath = settings.SETTINGS_ROOT + abpath

    print "convert_smile_png"
    print fullpath
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
    print singletask


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
        singletask.image = SearchEngineModel.objects.get(smiles__contains=task.file_obj.smiles).image
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
