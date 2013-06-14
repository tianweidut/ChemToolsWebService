# coding: UTF-8
'''
Created on 2013-04-03

@author: tianwei

Desc: custom 403, 404, 500 page
'''
from django.shortcuts import render_to_response
from django.shortcuts import render


def error403(request):
    """
    403 page
    """
    return render(request, "utility/403.html")


def error404(request):
    """
    404 page
    """
    return render(request, "utility/404.html")


def error500(request):
    """
    500 page
    """
    return render(request, "utility/500.html")
