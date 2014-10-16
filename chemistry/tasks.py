# coding: UTF-8
import os
import json
import datetime

from celery.decorators import task
from django.conf import settings
from django.core.files import File
from django.contrib.sites.models import Site
from django.core.mail import send_mail

from chemistry.calcore.prediciton_model import prediction_model_calculate
from chemistry.models import SingleTask, SuiteTask, StatusCategory
from chemistry import (STATUS_WORKING, STATUS_SUCCESS, STATUS_FAILED,
                       TASK_SUITE, TASK_SINGLE)
from chemistry.util import generate_mol_image, generate_pdf
from utils import chemistry_logger

LOCK_EXPIRE = 60 * 5  # Lock expires in 5 minutes
DEFAULT_TEMPERATURE_ARGS = 25  # 默认摄氏温度


def has_temperature(model_name):
    return model_name.lower() in ('koh_t', 'koa', 'pl')


def get_model_name(name):
    # 模型对应接口：
    # 前端:templates/newtask.html, model name (src)
    # 后端:chemistry/calcore/prediciton_model.py, models_computation (dest)
    model_map = {
        "koa": "logKOA",
        "rp": "logRP",
        "koc": "logKOC",
        "bcf": "logBCF",
        "koh": "logKOH",
        "koh_t": "logKOH_T",
        "pl": "logPL",
        "bdg": "logBDG",
    }

    model = model_map.get(name)
    if not model:
        raise KeyError("We don't have this model")

    return model


@task()
def add(x, y):
    return x + y


@task()
def add_counter(suite_id):
    """
    use filter to get task numbers
    """
    finished_count = SingleTask.objects.filter(sid=suite_id)\
                                       .exclude(status=StatusCategory.objects.get(category=STATUS_WORKING))\
                                       .count()
    suite = SuiteTask.objects.get(sid=suite_id)

    if finished_count == suite.total_tasks:
        suite.has_finished_tasks = suite.total_tasks
        suite.status_id = StatusCategory.objects.get(category=STATUS_SUCCESS)
        try:
            file_path = generate_pdf(id=suite_id, task_type=TASK_SUITE)
            f = File(open(file_path))
            suite.result_pdf = f
        except Exception:
            chemistry_logger.exception("failed to generate pdf")

        # send email
        send_email_task.delay(email=suite.email, sid=suite.sid)
        suite.end_time = datetime.datetime.now()
    else:
        suite.has_finished_tasks = finished_count

    suite.save()


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
        reports_list += "http://" + site.domain + \
            suitetask.result_pdf.url + "\n\r"
    task_lists = SingleTask.objects.filter(sid=sid)
    for task in task_lists:
        if task.result_pdf:
            reports_list += "http://" + site.domain + \
                task.result_pdf.url + "\n\r"

    message = "Congratulations! Your calculate task is Finished, please, check\
               the reports\n%s" % reports_list

    send_mail(subject, message,
              settings.DEFAULT_FROM_EMAIL, [email])


@task()
def calculateTask(task, model):
    try:
        generate_mol_image(task)
        suite = task.sid
        map_model_name = get_model_name(model['model'])
        smile = task.file_obj.smiles.encode('utf-8') if task.file_obj.file_type != 'mol' else ''

        # smile, mol_fpath 输入只选择一种方式(优先smile)
        mol_fpath = os.path.join(settings.SETTINGS_ROOT, task.file_obj.file_obj.path) if not smile else None

        temperature = float(model.get('temperature', DEFAULT_TEMPERATURE_ARGS))
        chemistry_logger.info('PredictionModel calculating: model name(%s),'
                              'smile(%s) mol path(%s) temperature(%s)',
                              map_model_name, smile, mol_fpath, temperature)
        # 重构入口
        predict_results = prediction_model_calculate(map_model_name, smile,
                                                     mol_fpath, temperature)

        if task.file_obj.file_type == 'mol':
            name = os.path.basename(mol_fpath).split('.')[0]
        else:
            name = smile
        result = predict_results[name][map_model_name]
        chemistry_logger.info('result %s' % result)
    except KeyError:
        chemistry_logger.exception('still cannot support this model')
        result = None
        task.result_state = "We don't support this model now"
        task.status = StatusCategory.objects.get(category=STATUS_FAILED)
        suite.status_id = StatusCategory.objects.get(category=STATUS_FAILED)
    except Exception as e:
        chemistry_logger.exception('failed to submit task to prediction model')
        result = None
        task.result_state = str(e)
        task.status = StatusCategory.objects.get(category=STATUS_FAILED)
        suite.status_id = StatusCategory.objects.get(category=STATUS_FAILED)
    else:
        chemistry_logger.info("calculate Successfully in celery queue!")
        task.result_state = "Calculate Successfully!"
        task.status = StatusCategory.objects.get(category=STATUS_SUCCESS)
        suite.status_id = StatusCategory.objects.get(category=STATUS_WORKING)

    suite.save()

    task.end_time = datetime.datetime.now()
    task.results = json.dumps(result)

    try:
        file_path = generate_pdf(id=task.pid, task_type=TASK_SINGLE)
        task.result_pdf = File(open(file_path, "rb"))
        task.save()
    except Exception:
        chemistry_logger.exception("failed to generate pdf")

    add_counter.delay(suite.sid)

    return result
