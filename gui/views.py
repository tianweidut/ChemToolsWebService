#coding: utf-8

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from gui import forms
from backend.fileoperator import upload_response
from backend.ChemSpiderPy.wrapper import search_cheminfo
from backend.logging import logger
from backend.utilities import *
from calcore.models import *
from const import MODEL_SPLITS
from const import ORIGIN_UPLOAD
from const.models import ModelCategory


@login_required
def multi_inputform(request):
    """
    Multi input form:
       * basic info search view function
         for STEP1 page and Search page
       * multi files upload
    """
    models = {model.category: model.desc for model in ModelCategory.objects.all()}

    if request.method == "POST" and request.FILES:
        return upload_response(request)

    return render(request, "features/newtask.html",
                           dict(models=models))


@login_required
def history_view(request):
    """
    """
    result_sets = SuiteTask.objects.filter(user__user=request.user).order_by('-start_time')

    #Add more attributes inito SuiteTask_list
    for task in result_sets:
        task.models_str_list = get_models_selector(task.models_str)
        task.models_category_str_list = get_models_selector(task.models_category_str)
        task.progress_value = "%0.2f"%(float(task.has_finished_tasks) / task.total_tasks * 100)
        task.is_finished = True if task.total_tasks == task.has_finished_tasks else False

    return render(request, 'features/history.html',
                  {'history_lists': result_sets})


#TODO: Add only user decorators
@login_required
def suite_details_view(request, sid=None):
    """
    Suitetask details view
    """
    suitetask = get_object_or_404(SuiteTask, sid=sid)
    single_lists = SingleTask.objects.filter(sid=sid)

    return render(request, 'features/details.html',
                  {"suitetask": suitetask,
                   "single_lists": single_lists})


def task_details_context(pid):
    """
    """
    singletask = get_object_or_404(SingleTask, pid=pid)

    try:
        search_engine = SearchEngineModel.objects.get(smiles=singletask.file_obj.smiles)
    except Exception, err:
        loginfo(p=err)
        search_engine = None

    re_context = {"singletask": singletask,\
                  "search_engine": search_engine}

    return re_context


#TODO: Add only user decorators
@login_required
def task_details_view(request, pid=None):
    """
    Every singletask details view
    """
    re_context = task_details_context(pid)

    return render(request, 'widgets/task_details.html', re_context)
