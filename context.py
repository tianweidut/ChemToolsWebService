"""
    Author:tianwei
    Email: liutianweidlut@gmail.com
    Desc: settings context processor for templates, 
          then we can use 
"""

from django.conf import settings

all_required = ()

def application_settings(request):
    """The context processor function"""
    mysettings = {}
    for keyword in all_required:
        mysettings[keyword] = getattr(settings, keyword)

    context = {
        'settings': mysettings,
    }

    return context
