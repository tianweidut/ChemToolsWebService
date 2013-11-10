#coding: utf-8
import json
from functools import wraps


def jsonize(func):
    @wraps
    def _(*a, **kw):
        content = func(*a, **kw)
        return json.dumps(content)
    return _
