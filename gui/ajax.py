# -*- coding: UTF-8 -*-
'''
Created on 2013-03-25

@author: tianwei

Desc: This module will be used for ajax request, such as form valid, search
      query, calculated submit.
'''

import simplejson
import uuid
import datetime
from dajaxice.decorators import dajaxice_register

from backend.logging import logger, loginfo
from backend.ChemSpiderPy.wrapper import search_cheminfo
from calcore.models import *
from backend.utilities import *
from gui.tasks import *


@dajaxice_register(method='GET')
@dajaxice_register(method='POST', name="calculate_submit_post")
def calculate_submit(request,
                     smile=None,
                     mol=None,
                     notes=None,
                     name=None,
                     email=None,
                     unique_names=None,
                     types="pdf;txt;csv",
                     models=None
                     ):
    #TODO: this is only for test, later we will delete this line
    add.delay(10, 10)

    is_submitted, message = suitetask_process(request, smile=smile, mol=mol,
                                              notes=notes, name=name,
                                              email=email,
                                              unique_names=unique_names,
                                              types=types,
                                              models=models)

    return simplejson.dumps({'message': message,
                             'is_submitted': is_submitted})


@dajaxice_register(method='GET')
@dajaxice_register(method='POST', name="search_varify_post")
def search_varify_info(request, query=None):
    # Calculated Submit Process
    logger.info(query)
    data = {}

    if query is not None:
        search_result = search_cheminfo(query.strip())
        data = {"is_searched": True,
                "search_result": search_result}
    else:
        data = {"is_searched": False,
                "search_result": "None"}
    logger.info(data)
    return simplejson.dumps(data)
