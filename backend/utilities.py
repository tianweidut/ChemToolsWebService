# coding: UTF-8
'''
Created on 2013-5-21

@author: tianwei

Desc: a source code tool
'''
import uuid
import simplejson

from django.http import HttpResponse


def get_sid():
    return str(uuid.uuid4())


def response_minetype(request):
    if "application/json" in request.META["HTTP_ACCEPT"]:
        return "application/json"
    else:
        return "text/plain"


class JSONResponse(HttpResponse):
    """Json response class"""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
