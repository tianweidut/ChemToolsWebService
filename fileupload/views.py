# -*- coding: UTF-8 -*-
'''
Created on 2013-01-20

@author: tianwei
'''

from django.views.generic import CreateView, DeleteView
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.conf import settings

from fileupload.models import Picture


def response_minetype(request):
    if "application/json" in request.META["HTTP_ACCEPT"]:
        return "application/json"
    else:
        return "text/plain"


class PictureCreateView(CreateView):
    model = Picture
    template_name = "features/bootcamp.html"
    
    def form_valid(self, form):
        self.object = form.save()
        f = self.request.FILES.get("file")
        data = [{'name':f.name,
                 'url':settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"),
                 'thumbnail_url':settings.MEDIA_URL + "pictures/" + f.name.replace(" ", "_"),
                 'delete_url':reverse("upload-delete", args=[self.object.id]),
                 "delete_type": "DELETE"}]

        response = JSONResponse(data, {}, response_minetype(self.request))
        response["Content-Dispostion"] = "inline; filename=files.json"

        return response


class PictureDeleteView(DeleteView):
    model = Picture
    template_name = "features/bootcamp.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        # TODO: add delete actual files in filesystem

        if request.is_ajax():
            response = JSONResponse(True, {}, response_minetype(self.request))
            response["Content-Dispostion"] = "inline; filename=files.json"
            return response
        else:
            # TODO: only for test, later I will use anthor url
            return HttpResponseRedict("/bootcamp")


class JSONResponse(HttpResponse):
    """Json response class"""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)
