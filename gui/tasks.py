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
from django.contrib.sites.models import Site
from django.core.files.uploadedfile import UploadedFile
from django.core.cache import cache
from django.utils.hashcompat import md5_constructor as md5
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site

from calcore.controllers.prediciton_model import PredictionModel
from backend.logging import logger, loginfo
from calcore.models import SingleTask, ProcessedFile, SuiteTask
from const.models import StatusCategory
from const import STATUS_WORKING, STATUS_SUCCESS, STATUS_FAILED, STATUS_UNDEFINED

import pybel
from calcore.models import *
from const import ORIGIN_DRAW, TASK_SUITE, TASK_SINGLE
from gui.utilities import *


def get_ModelName(name):
    temp={
            "koa":"logKOA",
            "rp":"logRP",
            "koc":"logKOC",
            "bcf":"logBCF",
            "koh":"logKOH",
            "koh_T":"logKOH_T",
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
        try:
            file_path = generate_pdf(id=suite_id, task_type=TASK_SUITE)
            print file_path
            f = File(open(file_path))
            suite.result_pdf = f
        except Exception, err:
            loginfo(p=err, label="generate pdf error!")

        #send email
        send_email_task.delay(email=suite.email, sid=suite.sid)
        suite.end_time = datetime.datetime.now()

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
def send_email_task(email, sid):
    """
    send result email to user
    """
    subject = "EST863 Calculate WebService Notification Emails"
    reports_list = ""
    site = Site.objects.get()
    suitetask = SuiteTask.objects.get(sid=sid)
    if suitetask.result_pdf:
        reports_list += "http://" + site.domain + suitetask.result_pdf.url + "\n\r"
    task_lists = SingleTask.objects.filter(sid=sid)
    for task in task_lists:
        if task.result_pdf:
            reports_list += "http://" + site.domain + task.result_pdf.url + "\n\r"

    message = "Congratulations! Your calculate task is Finished, please, check\
               the reports\n%s" % reports_list

    loginfo(p=message, label="Email Test")
    send_mail(subject,
               message,
               settings.DEFAULT_FROM_EMAIL,
               [email])


@task()
def calculateTask(task, model_name,arguments=None):
    """
    Calculate task
    """
    #Covert smiles, png
    print "**"*10, "generate smile image"
    generate_smile_image(task.pid)

    print "**"*10, "Models Calculate"
    para = dict.fromkeys(['smilestring', 'filename', 'cas'], "")

    fullpath = os.path.join(settings.SETTINGS_ROOT, task.file_obj.file_obj.path)
    print task.file_obj.file_type
    
    if task.file_obj.file_type=='mol':
        para['filename'] = os.path.basename(fullpath)
    else:
        para['smilestring']=task.file_obj.smiles.encode('utf-8')
        print task.file_obj.smiles
        
    filepath = os.path.dirname(fullpath)
    suite = task.sid
    result = 0

    print fullpath
    print para["filename"]
    print filepath

    try:
        print "---T----",arguments
        if arguments is None or arguments=='none':
            arguments='25'
            print "---afterT---",arguments
        pm =PredictionModel([get_ModelName(model_name)],para,filepath,float(arguments.encode('utf-8')))
        if task.file_obj.file_type=='mol':
            result =pm.predict_results[para['filename'].split(".")[0]][get_ModelName(model_name)]
        else:
            result=pm.predict_results[para['smilestring']][get_ModelName(model_name)]

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

    try:
        file_path = generate_pdf(id=task.pid, task_type=TASK_SINGLE)
        print file_path
        f = File(open(file_path, "rb"))
        task.result_pdf = f
    except Exception, err:
        loginfo(p=err, label="generate pdf error!")

    task.save()

    add_counter.delay(suite.sid)
    return result
