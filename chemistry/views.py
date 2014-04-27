#coding: utf-8

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from utils.file_operator import upload_response
from chemistry.util import (singletask_details, suitetask_details,
                            get_models_selector)
from chemistry.models import SuiteTask, ModelCategory


@csrf_exempt
@login_required
def submit(request):
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
def history(request):
    #TODO: Add pagination
    results = SuiteTask.objects.filter(user__user=request.user).order_by('-start_time')

    for r in results:
        r.models_str_list = get_models_selector(r.models_str)
        r.models_category_str_list = get_models_selector(r.models_category_str)
        r.progress_value = "%0.2f" % (float(r.has_finished_tasks) / r.total_tasks * 100)
        r.is_finished = bool(r.total_tasks == r.has_finished_tasks)

    return render(request, 'features/history.html',
                  dict(history_lists=results))


@login_required
def suitetask(request, sid=None):
    """
    Suitetask details view
    """
    return render(request, 'features/details.html',
                  suitetask_details(sid))


@login_required
def singletask(request, pid=None):
    """
    Every singletask details view
    """
    return render(request, 'widgets/task_details.html',
                  singletask_details(pid))
