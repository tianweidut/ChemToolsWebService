#coding: utf-8

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .utilities import jsonize
from backend.ChemSpiderPy.wrapper import search_cheminfo
from backend.fileoperator import upload_save_process
from backend.utilities import (singletask_details, suitetask_details,
                               summit_calculate)
from gui.utilities import search_cheminfo_local
from calcore.models import SuiteTask


@require_POST
@login_required
@jsonize
def login(request):
    if request.user.username:
        info = "login succeed"
        status = True
    else:
        info = "login failed"
        status = False

    return dict(info=info, status=status)


@require_POST
@login_required
@jsonize
def smile_search(request):
    query = request.POST.get('query', '')
    start = int(request.POST.get('start', 0))
    limit = int(request.POST.get('limit', 10))

    results_chemspider = search_cheminfo(query, start, limit)
    results_local = search_cheminfo_local(query, start, limit)
    search_results = results_local + results_chemspider

    results = []
    for r in search_results:
        c = dict(cas=r.cas,
                 forumula=r.forumula,
                 commonname=r.commonname,
                 smile=r.smiles,
                 alogp=r.alogp)
        results.append(c)

    return results


@require_POST
@login_required
@jsonize
def mol_upload(request):
    if request.method == "POST" and request.FILES:
        try:
            f = upload_save_process(request)
        except Exception as err:
            data = dict(status=False,
                        info=str(err),
                        uuid=None)
        else:
            data = dict(status=True,
                        info="upload file succeed",
                        uuid=f.fid,
                        name=f.title)
    else:
        data = dict(status=False,
                    uuid=None,
                    info='post file field is required')
    return data


@require_POST
@login_required
@jsonize
def task_submit(request):
    smile = request.POST.get('smile')
    draw = request.POST.get('draw')
    files = request.POST.get('files')
    models = request.POST.get('models')
    notes = request.POST.get('notes')
    name = request.POST.get('name')
    emails = request.POST.get('emails')

    try:
        status, info, id = summit_calculate(request.user,
            smile=smile, draw=draw, files=files, models=models,
            notes=notes, name=name, email=emails)
    except Exception as err:
        status, info, id = False, str(err), None

    return dict()


@require_POST
@login_required
@jsonize
def suitetask(request):
    id = request.POST.get('id')
    content = suitetask_details(id)
    details = content.get('suitetask')
    ret = details.__dict__
    ret.update(dict(models=details.models_str,
                    models_category=details.models_category_str,
                    result=details.result_pdf.url,
                    singletask_lists=[t.pid for t in content.get('single_lists')]))
    return ret


@require_POST
@login_required
@jsonize
def singletask(request):
    id = request.POST.get('id')
    details = singletask_details(id).get("singletask")
    ret = details.__dict__
    ret.update(result_file=details.result_pdf.url)
    ret.update(src_file=details.file_obj.url)
    return ret


@require_POST
@login_required
@jsonize
def history(request):
    start = int(request.POST.get('start', 0))
    limit = int(request.POST.get('limit', 30))

    #Django queryset is lazy, like iterator
    results = SuiteTask.objects.filter(user__user=request.user)\
                .order_by('-start_time')[start:(start+limit)]
    return dict(suitetask_lists=[r.sid for r in results])
