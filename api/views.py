#coding: utf-8

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .utilities import jsonize
from backend.ChemSpiderPy.wrapper import search_cheminfo
from backend.fileoperator import upload_save_process
from gui.utilities import search_cheminfo_local


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
    return dict()


@require_POST
@login_required
@jsonize
def suitetask(request):
    return dict()


@require_POST
@login_required
@jsonize
def singletask(request):
    return dict()


@require_POST
@login_required
@jsonize
def history(request):
    return dict()
