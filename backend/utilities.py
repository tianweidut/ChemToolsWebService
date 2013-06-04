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

from django.http import HttpResponse
from django.conf import settings
from django.core.files import File
import pybel

from backend.logging import loginfo
from calcore.models import SingleTask, ProcessedFile, MolFile, SuiteTask
from const.models import ModelCategory
from const import MODEL_KOA, MODEL_KOF, MODEL_PL
from const import MODEL_BCF, MODEL_PKD, MODEL_DFS
from const import MODEL_DFS
from const import ORIGIN_DRAW, ORIGIN_SMILE, ORIGIN_UPLOAD
from const import ORIGIN_OTHER, ORIGIN_UNDEFINED
from const.models import StatusCategory, FileSourceCategory
from const import STATUS_WORKING
from users.models import UserProfile
from calcore.controllers.prediciton_model import PredictionModel

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
    number = 0

    number = number + len(pid_list)
    number = number + 1 if smile else 0
    number = number + 1 if mol else 0

    if number == 0:
        return 0

    models_dict = parse_models(models)
    number = number * len(models_dict)

    loginfo(p=number, label="calculate_tasks")
    return number
def get_ModelName(name)
    temp={
            "koa":"logKOA"
            }
    if temp.has_key(name):
        return temp.get(name)

def save_record(f, model_name, sid, source_type, arguments=None):
    """
    Here, we use decoartor design pattern,
    this function is the real function
    """
    task = SingleTask()
    task.sid = SuiteTask.objects.get(sid=sid)
    task.pid = str(uuid.uuid4())
    #TODO: add arguments into task
    task.model = ModelCategory.objects.get(category=model_name)

    mol_file = MolFile()
    mol_file.sid = task.sid
    mol_file.name = model_name + str(uuid.uuid4())
    mol_file.file_obj = f
    mol_file.upload_time = datetime.datetime.now()
    mol_file.file_type = "mol"
    mol_file.file_size = f.size
    mol_file.file_source = FileSourceCategory.objects.get(category=source_type)
    mol_file.save()

    task.calculate_mol = mol_file
    task.save()
    #TODO: call task query process function filename needs path
    para=dict.fromkeys(['smilestring','filename','cas'])
    para['filename']=mol_file.file_obj
    pm=PredictionModel([get_ModelName(model_name)],para)
    print pm.predict_results


def get_FileObj_by_smiles(smile):
    """
    convert smile into mol file
    """
    name = str(uuid.uuid4()) + ".mol"
    name_path = os.path.join(settings.MOL_CONVERT_PATH, name)

    mol = pybel.readstring('smi', str(smile))
    mol.addh()
    mol.make3D()
    mol.write('mol', name_path, overwrite=True)

    f = File(open(name_path, "r"))

    return f


def start_files_task(files_list, model_name, sid, arguments=None):
    """
    start a group task from files list
    It will write a record into SingleTask and send this task
    into system-task query.
    First, it shoud read files_list and convert them into MolFile
    """
    for fid in files_list:
        record = ProcessedFile.objects.get(fid=fid)
        save_record(record.file_obj, model_name, sid, ORIGIN_UPLOAD, arguments)

    loginfo(p=model_name, label="finish start smile task")


def start_smile_task(smile, model_name, sid, arguments=None):
    """
    start a group task from smile string
    It will write a record into SingleTask and send this task
    into system-task query
    """
    f = get_FileObj_by_smiles(smile)
    save_record(f, model_name, sid, ORIGIN_SMILE, arguments)
    f.close()

    
    loginfo(p=model_name, label="finish start smile task")
    


def start_moldraw_task(moldraw, model_name, sid, arguments=None):
    """
    start a group task from mol string
    It will write a record into SingleTask and send this task
    into system-task query
    First it should write moldraw into a file and clear the useless lines
    """
    #TODO: maybe we should clear the first three lines which are chemwrite info
    name = str(uuid.uuid4()) + ".mol"
    path = os.path.join(settings.MOL_CONVERT_PATH, name)
    f = File(open(path, "w"))
    f.write(moldraw)

    save_record(f, model_name, sid, ORIGIN_DRAW, arguments)

    f.close()
    loginfo(p=model_name, label="finish start smile task")


def suitetask_process(request, smile=None, mol=None, notes=None,
                      name=None, unique_names=None, types=None,
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

    if total_tasks == 0:
        is_submitted = False
        message = "Please choice one model or input one search!"
        return (is_submitted, message)


    suite_task = SuiteTask()
    suite_task.sid = str(uuid.uuid4())
    suite_task.user = UserProfile.objects.get(user=request.user)
    suite_task.smiles = smile
    suite_task.total_tasks = int(total_tasks)
    suite_task.has_finished_tasks = 0
    suite_task.start_time = datetime.datetime.now()
    suite_task.end_time = datetime.datetime.now()
    suite_task.name = name
    suite_task.notes = notes
    suite_task.status = StatusCategory.objects.get(category=STATUS_WORKING)
    suite_task.save()

    loginfo(p="finish suite save")

    models_dict = parse_models(models)
    for key in models_dict:
        #TODO: add mol arguments
        start_smile_task(smile, key, suite_task.sid)
        start_moldraw_task(mol, key, suite_task.sid)
        start_files_task(pid_list, key, suite_task.sid)

    is_submitted = True
    message = "Congratulations to you! calculated task has been submitted!"

    return (is_submitted, message)
