# coding: UTF-8
import os
import uuid
import json
import datetime
from functools import wraps
from os.path import join

import pybel

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.files import File
from django.db.models import Q

from users.models import UserProfile
from chemistry.models import (SingleTask, SuiteTask, StatusCategory,
                              ProcessedFile, ModelCategory, FileSourceCategory,
                              ChemInfoLocal)
from chemistry import (TASK_SUITE, TASK_SINGLE,
                       ORIGIN_DRAW, ORIGIN_UPLOAD, ORIGIN_SMILE,
                       STATUS_WORKING, MODEL_SPLITS, STATUS_FAILED)
from utils import chemistry_logger
from celery.decorators import task


def suite_task_context(sid):
    try:
        suite_task = SuiteTask.objects.get(sid=sid)
    except Exception:
        chemistry_logger.exception('failed to get suite task: %s' % sid)
        suite_task = None
        single_task_lists = []
    else:
        single_task_lists = SingleTask.objects.filter(sid=sid)

    return dict(suite_task=suite_task,
                single_task_lists=single_task_lists)


def single_task_context(pid):
    try:
        single_task = SingleTask.objects.get(pid=pid)
        local_search_id = single_task.file_obj.local_search_id
        if local_search_id and isinstance(local_search_id, int):
            local_search = ChemInfoLocal.objects.get(local_search_id)
        else:
            local_search = None
    except Exception:
        chemistry_logger.exception('failed to get single task: %s' % pid)
        single_task = None
        local_search = None

    return dict(single_task=single_task, search_engine=local_search)


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


def generate_mol_image(singletask):
    """generate smile and image for task"""
    chemistry_logger.info('generate smile image %s' % singletask.pid)
    fpath = settings.SETTINGS_ROOT + singletask.file_obj.file_obj.url
    mol = pybel.readfile("mol", fpath).next()
    singletask.file_obj.smiles = ("%s" % mol).split("\t")[0]

    pname = str(uuid.uuid4()) + ".png"
    if not os.path.exists(settings.SEARCH_IMAGE_PATH):
        os.makedirs(settings.SEARCH_IMAGE_PATH)

    ppath = os.path.join(settings.SEARCH_IMAGE_PATH, pname)
    mol.draw(show=False, filename=ppath)

    f = File(open(ppath, "r"))
    singletask.file_obj.image = f
    singletask.file_obj.save()
    singletask.save()
    f.close()


def simple_search_output(func):
    @wraps(func)
    def _(*a, **kw):
        rs = func(*a, **kw)
        rs = [dict(id=r.id,
                   cas=r.cas, smiles=r.smiles,
                   commonname=r.einecs_name,
                   formula=r.molecular_formula,
                   alogp=r.alogp) for r in rs]
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
    """get models name and color flag"""
    colors = ("label-success", "label-warning", "label-primary",
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
    from chemistry.tasks import has_temperature
    single_task = get_object_or_404(SingleTask, pid=pid)
    if not has_temperature(single_task.model.desc):
        single_task.temperature = '--'
    single_task.result_value, single_task.hi, single_task.hx = get_singletask_area(single_task.results)
    try:
        local_search_id = single_task.file_obj.local_search_id
        if local_search_id:
            local_search = ChemInfoLocal.objects.get(id=local_search_id)
        else:
            local_search = None
    except Exception:
        chemistry_logger.exception('failed to get cheminfo by local_search_id')
        local_search = None

    return dict(singletask=single_task,
                search_engine=local_search)


def suitetask_details(sid):
    from chemistry.tasks import has_temperature
    suitetask = get_object_or_404(SuiteTask, sid=sid)
    single_lists = SingleTask.objects.filter(sid=sid)

    for s in single_lists:
        if not has_temperature(s.model.desc):
            s.temperature = '--'
        s.result_value, s.hi, s.hx = get_singletask_area(s.results)

    return dict(suitetask=suitetask,
                single_lists=single_lists)


def get_singletask_area(data):
    try:
        data = json.loads(data)
    except:
        data = {}

    if not isinstance(data, dict):
        data = {'value': data}

    return (data.get('value', '--'), data.get('hi'), data.get('hx'))


def calculate_tasks(files_id_list, smile, mol_data, models):
    number = len(files_id_list)
    number += 1 if smile else 0
    number += 1 if mol_data else 0

    return number * len(models)


class ErrorCalculateType(Exception):
    pass


def save_record(f, model, sid, source_type, smile=None, local_search_id=None):
    from chemistry.tasks import calculateTask, DEFAULT_TEMPERATURE_ARGS
    task = SingleTask()
    task.sid = SuiteTask.objects.get(sid=sid)
    task.pid = str(uuid.uuid4())
    task.model = ModelCategory.objects.get(category=model['model'])

    temperature = model.get('temperature')
    task.temperature = float(temperature) if temperature else DEFAULT_TEMPERATURE_ARGS

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

        if source_type == ORIGIN_SMILE and local_search_id is not None:
            processed_f.local_search_id = int(local_search_id)

        processed_f.save()
        task.file_obj = processed_f
        obj.close()
    else:
        raise ErrorCalculateType('Cannot recongize this source type')

    task.status = StatusCategory.objects.get(category=STATUS_WORKING)
    task.save()

    calculateTask.delay(task, model)


def handle_files_task(files_id_list, model, sid):
    if not files_id_list or not isinstance(files_id_list, list):
        return

    for fid in files_id_list:
        if not fid:
            continue

        #根据id，获取前端页面上传的文件model
        f_record = ProcessedFile.objects.get(fid=fid)
        if f_record.file_type.lower() in ('mol', 'sdf'):
            save_record(f_record, model, sid, ORIGIN_UPLOAD)
        elif f_record.file_type.lower() in ('smi', 'cas'):
            handle_batch_file_task(f_record, sid, model)


def handle_batch_file_task(f_record, sid, model):
    # 只添加成功的任务，对失败的输入直接过滤掉
    cnt = 0
    path = join(settings.SETTINGS_ROOT, f_record.file_obj.path)
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip().strip('\n')
            try:
                # TODO: 需要检测是否符合格式
                if f_record.file_type.lower() == 'cas':
                    smile = get_smile_by_cas(line)
                else:
                    smile = line

                handle_smile_task(smile, model, sid)
            except:
                chemistry_logger.error('failed to submit %s' % line)
            else:
                cnt += 1
        else:
            s = SuiteTask.objects.get(sid=sid)
            s.total_tasks = s.total_tasks + cnt - 1
            s.save()
            chemistry_logger.info('update tasks cnt %s', s.total_tasks)


def get_smile_by_cas(cas):
    cas = cas.lstrip('0')
    result = ChemInfoLocal.objects.get(cas=cas)
    return result.smiles


def handle_smile_task(smile, model, sid, local_search_id=None):
    if not smile:
        return

    # 根据smile码计算mol文件，返回文件路径
    if not os.path.exists(settings.MOL_CONVERT_PATH):
        os.makedirs(settings.MOL_CONVERT_PATH)
    fpath = os.path.join(settings.MOL_CONVERT_PATH, "%s.mol" % uuid.uuid4())

    mol = pybel.readstring('smi', str(smile))
    mol.addh()
    mol.make3D()
    mol.write('mol', fpath, overwrite=True)

    save_record(fpath, model, sid, ORIGIN_SMILE, smile, local_search_id)


def handle_moldraw_task(moldraw, model, sid):
    if not moldraw:
        return

    fpath = os.path.join(settings.MOL_CONVERT_PATH, "%s.mol" % uuid.uuid4())
    f = File(open(fpath, "w"))
    f.write(moldraw)
    f.close()

    # 根据前端绘图产生的mol数据，写入本地文件，向后端传入文件路径
    save_record(fpath, model, sid, ORIGIN_DRAW)


def get_model_category(model_name):
    try:
        category = ModelCategory.objects.get(category=model_name).\
            origin_type.get_category_display()
    except Exception:
        chemistry_logger.exception('failed to get model category')
        category = ""

    return category


def parse_models(models):
    """
    Parse models json into models name and models type name
    Out: (models_str, models_category_str)
    """
    categorys = set()
    models_name = []
    for m in models:
        categorys.add(get_model_category(m['model']))
        models_name.append(m['model'])

    models_str = MODEL_SPLITS.join(models_name)
    categorys_str = MODEL_SPLITS.join(list(categorys))

    return (models_str, categorys_str)


def submit_calculate_task(user, smile=None, draw_mol_data=None,
                          task_notes=None, task_name=None,
                          files_id_list=None, models=None,
                          local_search_id=None):

    chemistry_logger.info("smile: %s" % smile)
    chemistry_logger.info("draw_mol_data: %s" % draw_mol_data)
    chemistry_logger.info("files_id_list: %s" % files_id_list)
    chemistry_logger.info("models: %s" % models)

    tasks_num = calculate_tasks(files_id_list, smile, draw_mol_data, models)

    if tasks_num == 0:
        status = False
        info = "请至少选择一种输入方式和计算模型!"
        id = None
        return (status, info, id)

    try:
        s = SuiteTask()
        s.sid = id = str(uuid.uuid4())
        s.user = UserProfile.objects.get(user=user)
        s.total_tasks = tasks_num
        s.has_finished_tasks = 0
        s.name = task_name
        s.notes = task_notes
        s.models_str, s.models_category_str = parse_models(models)
        s.status = StatusCategory.objects.get(category=STATUS_WORKING)
        s.email = user.email
        s.save()

        generate_calculate_task.delay(models, smile, draw_mol_data,
                                      files_id_list, id, local_search_id)
    except:
        chemistry_logger.exception('failed to generate suite_task')
        s.delete()
        status = False
        info = "计算任务添加不成功，将重试或联系网站管理员!"
        id = None
    else:
        status = True
        info = "恭喜,计算任务已经提交!"

    return (status, info, id)


@task
def generate_calculate_task(models, smile, draw_mol_data, files_id_list,
                            sid, local_search_id):
    from chemistry.tasks import send_email_task
    try:
        for model in models:
            handle_smile_task(smile, model, sid, local_search_id)
            handle_moldraw_task(draw_mol_data, model, sid)
            handle_files_task(files_id_list, model, sid)
    except Exception:
        chemistry_logger.exception('failed to generate suite_task:%s' % sid)
        s = SuiteTask.objects.get(sid=sid)
        s.end_time = datetime.datetime.now()
        s.status_id = StatusCategory.objects.get(category=STATUS_FAILED)
        s.save()
        send_email_task.delay(s.email, s.sid)
