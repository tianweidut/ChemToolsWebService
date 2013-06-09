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
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import UploadedFile
from calcore.controllers.prediciton_model import PredictionModel
from backend.logging import logger
from calcore.models import SingleTask, ProcessedFile, MolFile, SuiteTask

def get_ModelName(name):
    temp={
            "koa":"logKOA",
            "pl":"logRP",
            }
    if temp.has_key(name):
        return temp.get(name)

@task()
def add(x, y):
    print "sleep!"
    return x+y+x+y

@task()
def add_a(x, y):
    print "sleep! a"
    return x+y+x+y

@task()
def calculateTask(f,task,model_name):
    molpath=os.path.split(f.name)[0]
    print molpath
    para=dict.fromkeys(['smilestring','filename','cas'],"")
    #para['filename']=model_name+str(uuid.uuid4())+".mol"
    #para['smilestring']=""
    #para['cas']=""
    para['filename']=os.path.split(f.name)[1]
    print para
    pm=PredictionModel([get_ModelName(model_name)],para,molpath)
    result= pm.predict_results[os.path.split(f.name)[1].split(".")[0]][get_ModelName(model_name)]
    print result
    #task=SingleTask.objects.get(pid=pid)
    task.results=result
    task.save()
    #suite=SuiteTask.objects.get(sid=task.sid)
    suite=task.sid
    suite.has_finished_tasks+=1
    suite.save()
    return result
