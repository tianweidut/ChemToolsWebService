"""
    Author:tianwei
    Email: liutianweidlut@gmail.com
    Desc: settings context processor for templates, 
          then we can use 
"""

from django.conf import settings

from users.models import UserGrade, UserProfile
from calcore.models import *
from const import STATUS_SUCCESS

all_required = ("PRODUCTION_FLAG",)


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
        context["data_context"]["remain_num"] = profile.user_grade.total_num - finished_num

    except:
        pass

    return context
