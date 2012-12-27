"""
    Author:tianwei
    Email: liutianweidlut@gmail.com
    Desc: settings context processor for templates, 
          then we can use 
"""

from django.conf import settings

all_required = (
                'MAX_TAG_LENGTH',
                'TAGS_ARE_REQUIRED',
                'MAX_COMMENT_LENGTH',
                'ENABLE_TAG_MODERATION',
                'TAGS_ARE_REQUIRED',
                'MAX_TAGS_PER_POST',
                'SHOW_LOGO',
                'USE_LICENSE',
                'LICENSE_USE_URL',
                'LICENSE_USE_LOGO',
                'LICENSE_ACRONYM',
                'LICENSE_TITLE',
                'LICENSE_URL',
                'LICENSE_LOGO_URL',
                'APP_COPYRIGHT',
                'APP_TITLE',
                'SITE_LOGO_URL',
                'LOGOUT_REDIRECT_URL',
                'LOGOUT_URL',
                )

def application_settings(request):
    """The context processor function"""
    mysettings = {}
    for keyword in all_required:
        mysettings[keyword] = getattr(settings,keyword)

    context = {
        'settings':mysettings,
    }

    return context

