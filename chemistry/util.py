# coding: UTF-8
import datetime
import re
import os
import uuid
from functools import wraps

import pybel
import xhtml2pdf.pisa as pisa
import cStringIO as StringIO

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files import File
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q

from users.models import UserProfile
from util import loginfo
from chemistry.models import (SingleTask, SuiteTask, StatusCategory,
                              ProcessedFile, ModelCategory, FileSourceCategory,
                              ChemInfoLocal, SearchEngineModel, ORIGIN_SMILE)
from chemistry import (STATUS_SUCCESS, TASK_SUITE, TASK_SINGLE,
                       ORIGIN_DRAW, ORIGIN_UPLOAD,
                       STATUS_WORKING, MODEL_SPLITS)

LOCK_EXPIRE = 60 * 5  # Lock expires in 5 minutes


def suite_details_context(sid):
    suitetask = get_object_or_404(SuiteTask, sid=sid)

    suitetask = get_object_or_404(SuiteTask, sid=sid)
    single_lists = SingleTask.objects.filter(sid=sid)

    re_context = {"suitetask": suitetask,
                  "single_lists": single_lists}

    return re_context


def task_details_context(pid):
    singletask = get_object_or_404(SingleTask, pid=pid)

    try:
        search_engine = SearchEngineModel.objects.get(
            smiles=singletask.file_obj.smiles)
    except Exception as err:
        loginfo(p=err)
        search_engine = None

    re_context = {"singletask": singletask,
                  "search_engine": search_engine}

    return re_context


def fetch_resources(uri, rel):
    """
    change pisa resource url to retrive
    pictures, css etc.
    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(
                settings.MEDIA_URL,
                ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(
            settings.STATIC_ROOT,
            uri.replace(
                settings.STATIC_URL,
                ""))
    else:
        path = os.path.join(
            settings.STATIC_ROOT,
            uri.replace(
                settings.STATIC_URL,
                ""))

        if not os.path.isfile(path):
            path = os.path.join(
                settings.MEDIA_ROOT,
                uri.replace(
                    settings.MEDIA_URL,
                    ""))

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
    except Exception as err:
        loginfo(p=err, label="cannot generate pdf")

    return path


def pdf_create_test():
    """
    pdf test create
    """
    task_id_search = "06b4c9a5-3a01-4bb4-a07c-d574d293d7e5"
    task_id_draw = "0a72a6ba-63f0-41db-a04f-f71c292f6db8"
    task_id_upload = "1142ae41-9497-4771-9c1c-d4dfcece994a"
    task_id_ch = "17673ac1-17dd-4f0d-958a-4ef44bba8a92"
    suite_id = "c933deb5-beda-4a41-84be-759a5795aca1"

    print "search type for single task"
    generate_pdf(id=task_id_search, task_type=TASK_SINGLE)
    print "draw type for single task"
    generate_pdf(id=task_id_draw, task_type=TASK_SINGLE)
    print "upload type for single task"
    generate_pdf(id=task_id_upload, task_type=TASK_SINGLE)
    print "not found this task id"
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
        # this type has already have image and smiles in local search machine,
        # only copy them
        singletask.file_obj.image = SearchEngineModel.objects.get(
            smiles=singletask.file_obj.smiles).image
        singletask.file_obj.save()
        singletask.save()
    else:
        # other types only contains mol file
        print "other input method"
        convert_smile_png(singletask)


def add_counter_core(suite_id):
    """
    core counter algorightm
    """
    print "add counter"
    suite = SuiteTask.objects.get(sid=suite_id)
    if suite.has_finished_tasks < suite.total_tasks - 1:
        suite.has_finished_tasks = suite.has_finished_tasks + 1
        print "add:" + str(suite.has_finished_tasks)
    else:
        suite.has_finished_tasks = suite.total_tasks
        print "Finished:" + str(suite.has_finished_tasks)
        print suite.has_finished_tasks
        suite.status_id = StatusCategory.objects.get(category=STATUS_SUCCESS)
        # generate suite task report and send email
    suite.save()


def simple_search_output(func):
    @wraps(func)
    def _(*a, **kw):
        rs = func(*a, **kw)
        rs = [dict(cas=r.cas, smiles=r.smiles,
                   commonname=r.einecs_name,
                   formula=r.molecular_formula,
                   alogp=r.alogp) for r in rs]
        return rs
    return _


def simple_search_output_api(func):
    @wraps(func)
    def _(*a, **kw):
        rs = func(*a, **kw)
        rs = [dict(cas="", smiles=r['content']['smiles'],
                   commonname=r['content']['commonname'],
                   formula=r['content']['mf'],
                   alogp=r['content']['alogp']) for r in rs]
        return rs
    return _


@simple_search_output
def search_cheminfo_local(query, start=0, limit=10):
    q = Q(cas=query) | \
        Q(smiles__contains=query) | \
        Q(molecular_formula=query)

    results = ChemInfoLocal.objects.filter(q)[start:(start + limit)]
    return results


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


def singletask_details(pid):
    singletask = get_object_or_404(SingleTask, pid=pid)

    try:
        search_engine = SearchEngineModel.objects.get(
            smiles=singletask.file_obj.smiles)
    except Exception:
        search_engine = None

    return dict(singletask=singletask,
                search_engine=search_engine)


def suitetask_details(sid):
    suitetask = get_object_or_404(SuiteTask, sid=sid)
    single_lists = SingleTask.objects.filter(sid=sid)

    return dict(suitetask=suitetask,
                single_lists=single_lists)


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

    number = number * len(models)

    loginfo(p=number, label="calculate_tasks")
    return number


def save_record(f, model_name, sid, source_type, smile=None, arguments=None):
    """
    Here, we use decoartor design pattern,
    this function is the real function
    """
    from chemistry.task import calculateTask
    task = SingleTask()
    task.sid = SuiteTask.objects.get(sid=sid)
    task.pid = str(uuid.uuid4())
    # TODO: add arguments into task
    task.model = ModelCategory.objects.get(category=model_name)

    if source_type == ORIGIN_UPLOAD:
        # here, f is ProcessedFile record instance
        f.file_source = FileSourceCategory.objects.get(category=source_type)
        f.file_type = "mol"
        task.file_obj = f
        f.save()
        task.status = StatusCategory.objects.get(category=STATUS_WORKING)
        task.save()
        calculateTask.delay(task, model_name)
    elif source_type == ORIGIN_SMILE or source_type == ORIGIN_DRAW:
        # here, f is a file path
        processed_f = ProcessedFile()
        obj = File(open(f, "r"))
        processed_f.title = os.path.basename(obj.name)
        processed_f.file_type = source_type
        processed_f.file_source = FileSourceCategory.objects.get(
            category=source_type)
        processed_f.file_obj = obj
        if smile:
            processed_f.smiles = smile
            # TODO: add database search local picture into here
        processed_f.save()
        task.file_obj = processed_f
        obj.close()
        task.status = StatusCategory.objects.get(category=STATUS_WORKING)
        task.save()
        calculateTask.delay(task, model_name, arguments)
    else:
        loginfo(p=source_type, label="Cannot recongize this source type")
        return

    # TODO: call task query process function filename needs path
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
    # TODO: maybe we should clear the first three lines which are chemwrite
    # info
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
    try:
        category = ModelCategory.objects.get(category=model_name).\
            origin_type.get_category_display()
    except Exception as err:
        loginfo(err)
        loginfo(model_name)
        category = ""

    return category


def get_models_name(models):
    """
    Parse models json into models name and models type name,
    which are CSV format, use MODEL_SPLITS in const.__init__

    Out: a tuple, models_str + models_category_str
    """
    categorys = set()
    models_name = []
    for m in models:
        categorys.add(get_model_category(m['model']))
        models_name.append(m['model'])

    models_str = MODEL_SPLITS.join(models_name)
    categorys_str = MODEL_SPLITS.join(list(categorys))

    return (models_str, categorys_str)


def get_email(email=None, backup_email=None):
    if bool(re.match(r"^.+@([a-zA-Z0-9]+\.)+([a-zA-Z]{2,})$", email)):
        return email
    else:
        # TODO: here, we should add email force-varify in registration page
        return backup_email


def submit_calculate(user, smile=None, mol=None, notes=None,
                     name=None, email=None, unique_names=None,
                     models=None):
    """
    real record operation
    Out:
        status, True or False
        message: summit message
    """

    total_tasks = calculate_tasks(unique_names, smile, mol, models)

    if total_tasks == 0:
        status = False
        info = "Please choice one model or input one search!"
        id = None
        return (status, info, id)

    suite_task = SuiteTask()
    suite_task.sid = str(uuid.uuid4())
    suite_task.user = UserProfile.objects.get(user=user)
    suite_task.total_tasks = int(total_tasks)
    suite_task.has_finished_tasks = 0
    suite_task.start_time = datetime.datetime.now()
    suite_task.end_time = datetime.datetime.now()
    suite_task.name = name
    suite_task.notes = notes
    suite_task.models_str, suite_task.models_category_str = get_models_name(
        models)
    suite_task.status = StatusCategory.objects.get(category=STATUS_WORKING)
    suite_task.email = get_email(email, user.email)
    suite_task.save()

    loginfo(p="finish suite save")

    flag = False
    try:
        for m in models:
            flag = flag | start_smile_task(
                smile,
                m['model'],
                suite_task.sid,
                m['temperature'])
            flag = flag | start_moldraw_task(
                mol,
                m['model'],
                suite_task.sid,
                m['temperature'])
            flag = flag | start_files_task(
                unique_names,
                m['model'],
                suite_task.sid,
                m['temperature'])
    except Exception as err:
        loginfo(err)
        flag = False

    if flag:
        status = True
        info = "Congratulations to you! calculated task has been submitted!"
        id = suite_task.sid
    else:
        status = False
        info = "No one tasks can be added into calculated task queue successful!"
        suite_task.delete()
        id = None

    return (status, info, id)


def get_model_name(name):
    temp = {
        "koa": "logKOA",
        "rp": "logRP",
        "koc": "logKOC",
        "bcf": "logBCF",
        "koh": "logKOH",
        "koh_T": "logKOH_T",
    }
    if name in temp:
        return temp.get(name)
    else:
        raise KeyError("We don't have this model")
