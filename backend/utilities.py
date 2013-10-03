# coding: UTF-8
'''
Created on 2013-5-21

@author: tianwei

Desc: a source code tool
'''
import uuid
import os
import simplejson
import datetime
import re

from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
import pybel

from backend.logging import loginfo
from calcore.models import SingleTask, ProcessedFile, SuiteTask
from const.models import ModelCategory
from const import MODEL_KOA, MODEL_KOF, MODEL_PL, MODEL_KOC, MODEL_KOH, MODEL_KOH_T, MODEL_RP
from const import MODEL_BCF, MODEL_PKD, MODEL_DFS
from const import MODEL_DFS
from const import ORIGIN_DRAW, ORIGIN_SMILE, ORIGIN_UPLOAD
from const import ORIGIN_OTHER, ORIGIN_UNDEFINED
from const.models import StatusCategory, FileSourceCategory
from const import STATUS_WORKING
from const import MODEL_SPLITS
from users.models import UserProfile
from calcore.controllers.prediciton_model import PredictionModel
from gui.tasks import *


def response_minetype(request):
    if "application/json" in request.META["HTTP_ACCEPT"]:
        return "application/json"
    else:
        return "text/plain"


class JSONResponse(HttpResponse):
    """Json response class"""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def make_uniquenames(name_str=None):
    """
    This function can process the unique name which is splited by
    comma
    Arguments:
        In: name_str, which is a comma strings
        Out: fid list, which are the primary key in ProcessedFile table
    """
    if name_str is None:
        return []

    fid_list = name_str.strip(";").split(";")

    loginfo(p=fid_list, label="make_uniquenames")

    return fid_list


def parse_models(model_str):
    """
    Parse models string
    Arguments:
        In: a list like [u'koa;none;80;none', u'kof;none;80;none']
        Out: a complex dict
    """

    loginfo(model_str)
    ret = {}
    if not model_str:
        return ret

    for item in model_str:
        item = item.split(";")
        ret[item[0]] = {}
        ret[item[0]]["temp"] = item[1]
        ret[item[0]]["humdity"] = item[2]
        ret[item[0]]["other"] = item[3]

    loginfo(p=ret, label="parse_models")
    return ret


def calculate_tasks(pid_list, smile, mol, models):
    """
    Calculate all tasks
    """
    loginfo(p=pid_list, label="files")
    loginfo(p=smile, label="smile")
    loginfo(p=mol, label="mol")

    number = 0
    if len(pid_list) != 1 or pid_list[0] != "":
        number = len(pid_list)

    number = number + (1 if smile else 0)
    number = number + (1 if mol else 0)

    if number == 0:
        return 0

    models_dict = parse_models(models)
    number = number * len(models_dict)

    loginfo(p=number, label="calculate_tasks")
    return number


def save_record(f, model_name, sid, source_type, smile=None, arguments=None):
    """
    Here, we use decoartor design pattern,
    this function is the real function
    """

    task = SingleTask()
    task.sid = SuiteTask.objects.get(sid=sid)
    task.pid = str(uuid.uuid4())
    #TODO: add arguments into task
    task.model = ModelCategory.objects.get(category=model_name)

    if source_type == ORIGIN_UPLOAD:
        #here, f is ProcessedFile record instance
        f.file_source = FileSourceCategory.objects.get(category=source_type)
        f.file_type = "mol"
        task.file_obj = f
        f.save()
        task.status = StatusCategory.objects.get(category=STATUS_WORKING)
        task.save()
        path = os.path.join(settings.MEDIA_ROOT, f.file_obj.url)
        calculateTask.delay(task, model_name)
    elif source_type == ORIGIN_SMILE or source_type == ORIGIN_DRAW:
        #here, f is a file path
        processed_f = ProcessedFile()
        obj = File(open(f, "r"))
        processed_f.title = os.path.basename(obj.name)
        processed_f.file_type = source_type
        processed_f.file_source = FileSourceCategory.objects.get(category=source_type)
        processed_f.file_obj = obj
        if smile:
            processed_f.smiles = smile
            #TODO: add database search local picture into here
        processed_f.save()
        task.file_obj = processed_f
        obj.close()
        task.status = StatusCategory.objects.get(category=STATUS_WORKING)
        task.save()
        calculateTask.delay(task, model_name,arguments)
    else:
        loginfo(p=source_type, label="Cannot recongize this source type")
        return

    #TODO: call task query process function filename needs path
    #global molpathtemp


def get_FileObj_by_smiles(smile):
    """
    convert smile into mol file
    Output: file path
    """
    name = str(uuid.uuid4()) + ".mol"
    if not os.path.exists(settings.MOL_CONVERT_PATH):
        os.makedirs(settings.MOL_CONVERT_PATH)
    name_path = os.path.join(settings.MOL_CONVERT_PATH, name)

    mol = pybel.readstring('smi', str(smile))
    mol.addh()
    mol.make3D()
    mol.write('mol', name_path, overwrite=True)

    return name_path


def start_files_task(files_list, model_name, sid, arguments=None):
    """
    start a group task from files list
    It will write a record into SingleTask and send this task
    into system-task query.
    First, it shoud read files_list and convert them into MolFile
    """
    if len(files_list) == 1 and files_list[0] == "" or not files_list:

        loginfo(p=files_list,
                label="Sorry, we cannot calculate files")
        return False

    for fid in files_list:
        record = ProcessedFile.objects.get(fid=fid)
        loginfo(p=record, label="files upload")
        save_record(record, model_name, sid, ORIGIN_UPLOAD, arguments)

    loginfo(p=model_name, label="finish start files task")
    return True


def start_smile_task(smile, model_name, sid, arguments=None):
    """
    start a group task from smile string
    It will write a record into SingleTask and send this task
    into system-task query
    """
    if not smile:
        loginfo(p=smile,
                label="Sorry, we cannot calculate smiles")
        return False

    f = get_FileObj_by_smiles(smile)
    save_record(f, model_name, sid, ORIGIN_SMILE, smile, arguments)

    loginfo(p=model_name, label="finish start smile task")
    return True


def start_moldraw_task(moldraw, model_name, sid, arguments=None):
    """
    start a group task from mol string
    It will write a record into SingleTask and send this task
    into system-task query
    First it should write moldraw into a file and clear the useless lines
    """
    #TODO: maybe we should clear the first three lines which are chemwrite info
    if not moldraw:
        loginfo(p=moldraw,
                label="Sorry, we cannot calculate draw mol files")
        return False

    name = str(uuid.uuid4()) + ".mol"
    path = os.path.join(settings.MOL_CONVERT_PATH, name)
    f = File(open(path, "w"))
    f.write(moldraw)
    f.close()

    save_record(path, model_name, sid, ORIGIN_DRAW, arguments)

    os.remove(path)

    loginfo(p=model_name, label="finish start smile task")

    return True


def get_model_category(model_name):
    """
    """
    if not model_name:
        return None

    category = ModelCategory.objects.get(category=model_name).\
               origin_type.get_category_display()

    return category


def get_models_name(models=None):
    """
    Parse models json into models name and models type name,
    which are CSV format, use MODEL_SPLITS in const.__init__

    Out: a tuple, models_str + models_category_str
    """
    loginfo(p=models)
    if not models:
        return ("", "")

    models_list = [i.split(MODEL_SPLITS)[0] for i in models]
    category_set = dict()
    for i in models_list:
        category = get_model_category(i)
        category_set[category] = ""

    models_str = MODEL_SPLITS.join(models_list)
    loginfo(p=category_set)
    models_category_str = MODEL_SPLITS.join(category_set.keys())

    loginfo(p=models_str)
    loginfo(p=models_category_str)

    return (models_str, models_category_str)


def get_email(email=None, backup_email=None):
    """
    """
    if bool(re.match(r"^.+@([a-zA-Z0-9]+\.)+([a-zA-Z]{2,})$", email)):
        return email
    else:
        #TODO: here, we should add email force-varify in registration page
        return backup_email


def suitetask_process(request, smile=None, mol=None, notes=None,
                      name=None, email=None, unique_names=None, types=None,
                      models=None):
    """
    real record operation
    Out:
        is_submitted, True or False
        message: summit message
    """
    is_submitted = False
    message = None

    #TODO: we should check remaining counts
    if request.user.is_anonymous():
        is_submitted = False
        message = "anonymous auth failed!"
        return (is_submitted, message)

    pid_list = make_uniquenames(unique_names)
    total_tasks = calculate_tasks(pid_list, smile, mol, models)
    #TODO: Add suite id into ProcessedFile Model

    if total_tasks == 0:
        is_submitted = False
        message = "Please choice one model or input one search!"
        return (is_submitted, message)


    suite_task = SuiteTask()
    suite_task.sid = str(uuid.uuid4())
    suite_task.user = UserProfile.objects.get(user=request.user)
    suite_task.total_tasks = int(total_tasks)
    suite_task.has_finished_tasks = 0
    suite_task.start_time = datetime.datetime.now()
    suite_task.end_time = datetime.datetime.now()
    suite_task.name = name
    suite_task.notes = notes
    suite_task.models_str, suite_task.models_category_str = get_models_name(models)
    suite_task.status = StatusCategory.objects.get(category=STATUS_WORKING)
    suite_task.email = get_email(email, request.user.email)
    suite_task.save()

    loginfo(p="finish suite save")

    models_dict = parse_models(models)
    print models_dict
    flag = False
    for key in models_dict:
        #TODO: add mol arguments
        flag = flag | start_smile_task(smile, key,suite_task.sid,models_dict[key]['temp'])
        flag = flag | start_moldraw_task(mol, key,suite_task.sid,models_dict[key]['temp'])
        flag = flag | start_files_task(pid_list, key,suite_task.sid,models_dict[key]['temp'])

    if flag:
        is_submitted = True
        message = "Congratulations to you! calculated task has been submitted!"
    else:
        is_submitted = False
        message = "No one tasks can be added into calculated task queue successful!"
        suite_task.delete()

    return (is_submitted, message)


def get_models_selector(models_str):
    """
    get models name and color flag

    Out:
        a list, element is a two-tuple.
    """
    colors = ("badge-success", "badge-warning", "badge-important",
              "badge-info", "badge-inverse", " ")
    models_list = models_str.split(MODEL_SPLITS)

    result = []

    for i in range(0, len(models_list)):
        e = {}
        e["color"] = colors[i % len(colors)]
        e["value"] = models_list[i]
        result.append(e)

    return result
