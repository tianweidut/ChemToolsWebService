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


@dajaxice_register(method='GET')
@dajaxice_register(method='POST', name="calculate_submit_post")
def calculate_submit(request,
                     smile=None,
                     mol=None,
                     notes=None,
                     name=None,
                     unique_names=None,
                     types="pdf;txt;csv",
                     models=None
                     ):

    pid_list = make_uniquenames(unique_names)
    total_tasks = calculate_tasks(pid_list, smile, mol, models)

    if total_tasks == 0:
        return simplejson.dumps({'message': 'Please choice one model or input one search!',
                                 'is_submitted': False})

    suite_task = SuiteTask()
    suite_task.sid = str(uuid.uuid4())
    suite_task.user = request.user
    suite.smiles = smile
    suite.mol_graph = mol
    suite_task.total_tasks = total_tasks
    suite_task.has_finished_tasks = 0
    suite_task.start_time = datetime.datetime.now()
    suite_task.name = name
    suite_task.notes = notes
    suite_task.save()

    models_dict = parse_models(models)
    for key in models_dict:
        #TODO: add mol arguments
        start_smile_task(smile, key, suite_task.sid)
        start_moldraw_task(mol, key, suite_task.sid)
        start_files_task(pid_list, key, suite_task.sid)

    return simplejson.dumps({'message': 'tianwei hello world!',
                             'is_submitted': True})


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
