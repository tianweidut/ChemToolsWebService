#coding: utf-8
import json

from django.http import HttpResponse
from django.core.files.uploadedfile import UploadedFile

from chemistry.models import ProcessedFile


def split_file_name(name, sep="."):
    if sep in name:
        f, t = name.split(sep, 1)
    else:
        f, t = name, " "

    return (f, t)


def file_upload_save_process(request):
    f = request.FILES["file"]
    name, filetype = split_file_name(UploadedFile(f).name)
    obj = ProcessedFile()
    obj.title = name
    obj.file_type = filetype
    obj.file_obj = f
    obj.save()

    return obj


def file_upload_response(request):
    f = file_upload_save_process(request)
    data = [{'name': f.title,
             'id': f.fid,
             'type': f.file_type}]

    response = JSONResponse(data, {}, response_minetype(request))
    response["Content-Dispostion"] = "inline; filename=files.json"
    return response


def response_minetype(request):
    if "application/json" in request.META["HTTP_ACCEPT"]:
        return "application/json"
    else:
        return "text/plain"


class JSONResponse(HttpResponse):
    """Json response class"""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = json.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
