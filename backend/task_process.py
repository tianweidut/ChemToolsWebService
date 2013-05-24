# coding: UTF-8
'''
Created on 2013-5-21

@author: tianwei

Desc: a source code tool
'''
import uuid
import simplejson

from django.http import HttpResponse
import pybel

from backend.logging import loginfo
from calcore.models import SingleTask, ProcessedFile, MolFile, SuiteTask


def get_sid():
    return str(uuid.uuid4())


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

    fid_list = name_str.split(",")

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

    models = model_str.lstrip("[").rstrip("]").split(",")
    for item in models:
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


def start_files_task(files_list, model_name, sid, arguments=None):
    """
    start a group task from files list
    It will write a record into SingleTask and send this task
    into system-task query.
    First, it shoud read files_list and convert them into MolFile
    """
    pass


def start_smile_task(smile, model_name, sid, arguments=None):
    """
    start a group task from smile string
    It will write a record into SingleTask and send this task
    into system-task query
    """
    pass


def start_moldraw_task(moldraw, model_name, sid, arguments=None):
    """
    start a group task from mol string
    It will write a record into SingleTask and send this task
    into system-task query
    First it should write moldraw into a file and clear the useless lines
    """
    pass
