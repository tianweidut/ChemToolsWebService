# coding: utf-8
import json

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden

from utils import make_json_response, basic_auth_api
from utils.file_operator import file_upload_save_process
from chemistry.util import (singletask_details, suitetask_details,
                            submit_calculate_task, search_cheminfo_local)
from chemistry.models import SuiteTask


@require_POST
@csrf_exempt
def smile_search(request):
    if not basic_auth_api(request):
        return HttpResponseForbidden()

    query = dict(cas=request.POST.get('cas'),
                 smile=request.POST.get('smile'),
                 common_name_ch=request.POST.get('common_name_ch'),
                 common_name_en=request.POST.get('common_name_en'))

    # TODO: 开启分页
    start = int(request.POST.get('start', 0))
    limit = int(request.POST.get('limit', 10))

    # TODO: 目前只是使用本地搜索，未来重新开启第三方search API
    #results_chemspider = search_cheminfo(query, start, limit)
    results = search_cheminfo_local(query, start, limit)

    return make_json_response(results)


@require_POST
@csrf_exempt
def mol_upload(request):
    if not basic_auth_api(request):
        return HttpResponseForbidden()

    if request.method == "POST" and request.FILES:
        try:
            f = file_upload_save_process(request)
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
    return make_json_response(data)


@require_POST
@csrf_exempt
def task_submit(request):
    if not basic_auth_api(request):
        return HttpResponseForbidden()

    post = request.POST
    smile = post.get('smile')
    draw_mol_data = post.get('draw_mol_data')
    files_id_list = json.loads(post.get('files_id_list', "[]"))
    models = json.loads(post.get('models', "[]"))
    task_notes = post.get('task_notes')
    task_name = post.get('task_name')
    local_search_id = int(post.get('local_search_id', 0))

    try:
        status, info, id = submit_calculate_task(
            request.user,
            smile=smile,
            draw_mol_data=draw_mol_data,
            files_id_list=files_id_list,
            models=models,
            task_notes=task_notes,
            task_name=task_name,
            local_search_id=local_search_id)
    except Exception as err:
        status, info, id = False, str(err), None

    return make_json_response(dict(status=status,
                                   info=info,
                                   id=id))


@require_POST
@csrf_exempt
def suitetask(request):
    if not basic_auth_api(request):
        return HttpResponseForbidden()

    id = request.POST.get('id')
    content = suitetask_details(id)
    details = content.get('suitetask')
    ret = dict(start_time=str(details.start_time),
               end_time=str(details.end_time),
               total_tasks=details.total_tasks,
               has_finished_tasks=details.has_finished_tasks,
               name=details.name,
               notes=details.notes,
               email=details.email,
               status=str(details.status),
               models=details.models_str,
               models_category=details.models_category_str,
               result=details.result_pdf.url if details.result_pdf else None,
               singletask_lists=[t.pid for t in content.get('single_lists')])

    return make_json_response(ret)


@require_POST
@csrf_exempt
def singletask(request):
    if not basic_auth_api(request):
        return HttpResponseForbidden()

    id = request.POST.get('id')
    details = singletask_details(id).get("singletask")
    ret = dict(start_time=str(details.start_time),
               end_time=str(details.end_time),
               sid=str(details.sid),
               temperature=details.temperature,
               humidity=details.humidity,
               model=str(details.model),
               status=str(details.status),
               results=details.results,
               result_file=details.result_pdf.url if details.result_pdf else None,
               src_file=details.file_obj.file_obj.url if details.file_obj else None)

    return make_json_response(ret)


@require_POST
@csrf_exempt
def history(request):
    if not basic_auth_api(request):
        return HttpResponseForbidden()

    start = int(request.POST.get('start', 0))
    limit = int(request.POST.get('limit', 30))

    # Django queryset is lazy, like iterator
    results = SuiteTask.objects.filter(user__user=request.user)\
        .order_by('-start_time')[start:(start + limit)]
    data = dict(suitetask_lists=[r.sid for r in results])
    return make_json_response(data)
