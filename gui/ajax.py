# -*- coding: UTF-8 -*-
'''
Created on 2013-03-25

@author: tianwei

Desc: This module will be used for ajax request, such as form valid, search
      query, calculated submit.
'''
import simplejson
from dajaxice.decorators import dajaxice_register

from backend.logging import logger, loginfo
from backend.ChemSpiderPy.wrapper import search_cheminfo
from calcore.models import *
from backend.utilities import *
from gui.tasks import *
from gui.utilities import search_cheminfo_local


@dajaxice_register(method='GET')
@dajaxice_register(method='POST', name="calculate_submit_post")
def calculate_submit(request,
                     smile=None,
                     draw_mol=None,
                     notes=None,
                     task_name=None,
                     email=None,
                     files=None,
                     models=None):
    try:
        is_submitted, message = suitetask_process(request,
                                                  smile=smile,
                                                  mol=draw_mol,
                                                  notes=notes,
                                                  name=task_name,
                                                  email=email,
                                                  unique_names=files,
                                                  models=models)
    except Exception, err:
        loginfo(err)
        message = "Server maybe wrong!, please contact administrator."
        is_submitted = False

    return simplejson.dumps({'message': message,
                             'is_submitted': is_submitted})


@dajaxice_register(method='GET')
@dajaxice_register(method='POST', name="search_varify_post")
def search_varify_info(request, query=None):
    # Calculated Submit Process
    logger.info(query)
    data = {}

    if query is not None:
        results = search_cheminfo(query.strip())
        data = {"is_searched": True,
                "results": results}
    else:
        data = {"is_searched": False}
    logger.info(data)
    return simplejson.dumps(data)


@dajaxice_register(method='GET')
@dajaxice_register(method='POST', name="search_local")
def search_local(request, query=None):
    logger.info(query)
    data = {}

    if query is not None:
        results = search_cheminfo_local(query.strip())
        data = {"is_searched": True,
                "results": results}
    else:
        data = {"is_searched": False}
    logger.info(data)
    return simplejson.dumps(data)
