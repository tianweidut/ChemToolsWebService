# coding: UTF-8
import datetime
import os
import uuid
from functools import wraps

import pybel
import cStringIO as StringIO

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files import File
from django.template.loader import get_template
from django.template import Context
from django.db.models import Q

from users.models import UserProfile
from chemistry.models import (SingleTask, SuiteTask, StatusCategory,
                              ProcessedFile, ModelCategory, FileSourceCategory,
                              ChemInfoLocal, SearchEngineModel)
from chemistry import (STATUS_SUCCESS, TASK_SUITE, TASK_SINGLE,
                       ORIGIN_DRAW, ORIGIN_UPLOAD, ORIGIN_SMILE,
                       STATUS_WORKING, MODEL_SPLITS)
from utils import chemistry_logger



def suite_details_context(sid):
    return dict(suitetask=get_object_or_404(SuiteTask, sid=sid),
                single_lists=SingleTask.objects.filter(sid=sid))


def task_details_context(pid):
    singletask = get_object_or_404(SingleTask, pid=pid)

    try:
        search_engine = SearchEngineModel.objects.get(
            smiles=singletask.file_obj.smiles)
    except Exception:
        chemistry_logger.exception('failed to search model')
        search_engine = None

    return dict(singletask=singletask,
                search_engine=search_engine)


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
        chemistry_logger.info(task_type, "Cannot check the type")
        return

    html = template.render(context).encode("UTF-8")
    html = StringIO.StringIO(html)

    #FIXME: import new html2pdf lib
    import xhtml2pdf.pisa as pisa
    try:
        name = str(uuid.uuid4()) + ".pdf"
        path = os.path.join(settings.SEARCH_IMAGE_PATH, name)
        f = open(path, "w")
        pisa.CreatePDF(html, dest=f, encoding="UTF-8",
                       link_callback=fetch_resources)
        f.close()
        print "finish pdf generate"
    except Exception:
        chemistry_logger.exception('failed to generate pdf')

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

    generate_pdf(id=task_id_search, task_type=TASK_SINGLE)
    generate_pdf(id=task_id_draw, task_type=TASK_SINGLE)
    generate_pdf(id=task_id_upload, task_type=TASK_SINGLE)
    generate_pdf(id=task_id_ch, task_type=TASK_SINGLE)
    generate_pdf(id=suite_id, task_type=TASK_SUITE)


def convert_smile_png(singletask):
    """
    convert mol into smile and png
    """
    abpath = singletask.file_obj.file_obj.url
    fullpath = settings.SETTINGS_ROOT + abpath

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
        convert_smile_png(singletask)


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
    #TODO: 加入中文名称搜索
    #Q(common_name_ch__contains=query['common_name_ch']) |
    q = Q(cas=query['cas'].strip())
    if query['smile']:
        q |= Q(smiles=query['smile'].strip())
    if query['common_name_en']:
        q |= Q(einecs_name__contains=query['common_name_en'].strip())

    results = ChemInfoLocal.objects.filter(q)[start:(start + limit)]
    return results


def get_models_selector(models_str):
    """
    get models name and color flag

    Out:
        a list, element is a two-tuple.
    """
    colors = ("label-success", "label-warning",
              "label-primary",
              "label-info", "label-danger", "label-default")
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
    chemistry_logger.info('[file id list]: %s, [smile]: %s, [mol]: %s' %
                          (pid_list, smile, mol))

    number = 0
    if len(pid_list) != 1 or pid_list[0] != "":
        number = len(pid_list)

    number = number + (1 if smile else 0)
    number = number + (1 if mol else 0)

    if number == 0:
        return 0

    return number * len(models)


class ErrorCalculateType(Exception):
    pass


def save_record(f, model_name, sid, source_type, smile=None, arguments=None):
    from chemistry.tasks import calculateTask
    task = SingleTask()
    task.sid = SuiteTask.objects.get(sid=sid)
    task.pid = str(uuid.uuid4())
    task.model = ModelCategory.objects.get(category=model_name)

    if source_type == ORIGIN_UPLOAD:
        # here, f is ProcessedFile record instance
        f.file_source = FileSourceCategory.objects.get(category=source_type)
        f.file_type = "mol"
        task.file_obj = f
        f.save()
    elif source_type in (ORIGIN_SMILE, ORIGIN_DRAW):
        # here, f is a file path
        processed_f = ProcessedFile()
        obj = File(open(f, "r"))
        processed_f.title = os.path.basename(obj.name)
        processed_f.file_type = source_type
        processed_f.file_source = FileSourceCategory.objects.get(category=source_type)
        processed_f.file_obj = obj
        if smile:
            processed_f.smiles = smile
            # TODO: add database search local picture into here
        processed_f.save()
        task.file_obj = processed_f
        obj.close()
    else:
        raise ErrorCalculateType('Cannot recongize this source type')

    task.status = StatusCategory.objects.get(category=STATUS_WORKING)
    task.save()
    calculateTask.delay(task, model_name, arguments)


def get_fileobj_by_smiles(smile):
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
        return False

    for fid in files_list:
        record = ProcessedFile.objects.get(fid=fid)
        save_record(record, model_name, sid, ORIGIN_UPLOAD, arguments)

    return True


def start_smile_task(smile, model_name, sid, arguments=None):
    """
    start a group task from smile string
    It will write a record into SingleTask and send this task
    into system-task query
    """
    if not smile:
        return False

    f = get_fileobj_by_smiles(smile)
    save_record(f, model_name, sid, ORIGIN_SMILE, smile, arguments)

    return True


def start_moldraw_task(moldraw, model_name, sid, arguments=None):
    """
    start a group task from mol string
    It will write a record into SingleTask and send this task
    into system-task query
    First it should write moldraw into a file and clear the useless lines
    """
    if not moldraw:
        return False

    name = str(uuid.uuid4()) + ".mol"
    path = os.path.join(settings.MOL_CONVERT_PATH, name)
    f = File(open(path, "w"))
    f.write(moldraw)
    f.close()

    save_record(path, model_name, sid, ORIGIN_DRAW, arguments)

    os.remove(path)

    return True


def get_model_category(model_name):
    try:
        category = ModelCategory.objects.get(category=model_name).\
            origin_type.get_category_display()
    except Exception:
        chemistry_logger.exception('failed to get model category')
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


def submit_calculate(user, smile=None, draw_mol_data=None,
                     task_notes=None, task_name=None,
                     files_id_list=None, models=None):
    total_tasks = calculate_tasks(files_id_list, smile, draw_mol_data, models)

    if total_tasks == 0:
        status = False
        info = "请至少选择一种输入方式和计算模型!"
        id = None
        return (status, info, id)

    suite_task = SuiteTask()
    suite_task.sid = str(uuid.uuid4())
    suite_task.user = UserProfile.objects.get(user=user)
    suite_task.total_tasks = int(total_tasks)
    suite_task.has_finished_tasks = 0
    suite_task.start_time = datetime.datetime.now()
    suite_task.end_time = datetime.datetime.now()
    suite_task.name = task_name
    suite_task.notes = task_notes
    suite_task.models_str, suite_task.models_category_str = get_models_name(models)
    suite_task.status = StatusCategory.objects.get(category=STATUS_WORKING)
    suite_task.email = user.email
    suite_task.save()

    flag = False
    try:
        for m in models:
            flag = flag | start_smile_task(smile, m['model'], suite_task.sid, m['temperature'])
            flag = flag | start_moldraw_task(draw_mol_data, m['model'], suite_task.sid, m['temperature'])
            flag = flag | start_files_task(files_id_list, m['model'], suite_task.sid, m['temperature'])
    except Exception:
        chemistry_logger.exception('failed to suite task')
        flag = False

    if flag:
        status = True
        info = "恭喜,计算任务已经提交!"
        id = suite_task.sid
    else:
        status = False
        info = "计算任务添加不成功，将重试或联系网站管理员!"
        suite_task.delete()
        id = None

    return (status, info, id)
