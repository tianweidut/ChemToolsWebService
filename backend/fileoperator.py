#coding: utf-8
from django.core.files.uploadedfile import UploadedFile

from backend.utilities import JSONResponse, response_minetype
from calcore.models import ProcessedFile


def split_name(name, sep="."):
    """
        split type and name in a filename
    """
    if sep in name:
        f, t = name.split(sep, 1)
    else:
        f, t = name, " "

    return (f, t)


def upload_save_process(request):
    """
        save file into local storage
    """
    f = request.FILES["file"]
    wrapper_f = UploadedFile(f)

    name, filetype = split_name(wrapper_f.name)
    #TODO: we maybe check file type here!

    obj = ProcessedFile()
    obj.title = name
    obj.file_type = filetype
    obj.file_obj = f
    obj.save()

    return obj


def upload_response(request):
    """
        use AJAX to process file upload
    """
    f = upload_save_process(request)
    data = {'name': f.title,
            'id': f.fid,
            'type': f.file_type}

    response = JSONResponse(data, {}, response_minetype(request))
    response["Content-Dispostion"] = "inline; filename=files.json"

    return response
