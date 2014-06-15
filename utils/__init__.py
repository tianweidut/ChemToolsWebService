#coding: utf-8
import datetime
import time
import base64
import json
from functools import wraps

from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.utils.log import getLogger

logger = getLogger('django')
chemistry_logger = logger


def loginfo(p="", label=""):
    logger.info("***"*10)
    logger.info(label)
    logger.info(p)
    logger.info("---"*10)


def jsonize(func):
    @wraps
    def _(*a, **kw):
        content = func(*a, **kw)
        return json.dumps(content)
    return _


def make_json_response(data):
    data = json.dumps(data)
    return HttpResponse(data, mimetype='application/json')


def basic_auth_api(request):
    if request.user and not request.user.is_anonymous():
        return True

    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                try:
                    username, password = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username=username, password=password)
                    if user and not user.is_anonymous():
                        request.user = user
                        return True
                except Exception:
                    pass

    return False


def is_client(request):
    ua = request.META.get('HTTP_USER_AGENT', '') 
    chemistry_logger.info(ua)
    return 'python' in ua.lower() or 'main' in ua.lower() 


def get_real_now():
    #hack, only for mopac2012.exe expired
    d = datetime.datetime.now() + datetime.timedelta(days=365)
    s = time.mktime(d.timetuple())
    now = datetime.datetime.fromtimestamp(s)
    chemistry_logger.info('------nws get real now %s' % now)
    return now 
