#coding: utf-8
from django.conf import settings

from users.models import UserProfile
from chemistry import STATUS_SUCCESS
from chemistry.models import SuiteTask
from utils import is_client

all_required = ("PRODUCTION_FLAG",)


def client_settings(request):
    context = dict(is_client=is_client(request))

    return context


def application_settings(request):
    """The context processor function"""
    mysettings = {}
    for keyword in all_required:
        mysettings[keyword] = getattr(settings, keyword)

    context = {
        'settings': mysettings,
    }

    return context


def userinfo_context(request):
    """
    The context will show the users info for navbar
    """
    context = {"info_context": None,
               "data_context": {"query_num": None,
                                "remain_num": None}}

    if request.user.is_anonymous():
        return context

    try:
        profile = UserProfile.objects.get(user=request.user)
        context["info_context"] = profile
        """
        Design Tips: here, only the successful task is the finished task,
        so the remaining number like below!
        """
        finished_num = SuiteTask.objects.filter(user=request.user,
                                                status__category=STATUS_SUCCESS).count()
        query_num = SuiteTask.objects.filter(user=request.user,
                                             status__category=STATUS_WORKING).count()
        context["data_context"] = {}
        context["data_context"]["query_num"] = query_num

    except:
        pass

    return context
