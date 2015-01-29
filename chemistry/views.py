#coding: utf-8

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from utils import is_client, chemistry_logger
from utils.file_operator import file_upload_response
from chemistry.util import (singletask_details, suitetask_details,
                            get_models_selector)
from chemistry.models import SuiteTask, SingleTask


@csrf_exempt
@login_required
def submit(request):
    if request.method == "POST" and request.FILES:
        return file_upload_response(request)
    return render(request, "newtask.html")


@login_required
def history(request):
    #TODO: Add pagination
    results = SuiteTask.objects.filter(user__user=request.user,
            is_hide=False).order_by('-start_time')

    #show_all = request.META.get('show_all', '0') == '1'
    #if not show_all:
    #    pass
        #results = results.filter(is_hide=True)

    for r in results:
        r.models_str_list = get_models_selector(r.models_str)
        r.models_category_str_list = get_models_selector(r.models_category_str)
        r.progress_value = "%0.2f" % (float(r.has_finished_tasks) / r.total_tasks * 100)
        r.is_finished = bool(r.total_tasks == r.has_finished_tasks)

    return render(request, 'history.html',
                  dict(history_lists=results))


@login_required
def suitetask(request, sid=None):
    return render(request, 'suite_details.html',
                  suitetask_details(sid))


@login_required
def singletask(request, pid=None):
    return render(request, 'task_details.html',
                  singletask_details(pid))


@login_required
def hide(request, id):
    category = request.GET.get('category')
    if category == 'suite':
        rs = SuiteTask.objects.filter(sid=id)
    elif category == 'single':
        rs = SingleTask.objects.filter(pid=id)
    else:
        return HttpResponseRedirect('/history')

    chemistry_logger.info('hide %s %s' % (category, id))

    for r in rs:
        r.is_hide = True
        r.save()

    return HttpResponseRedirect('/history')
