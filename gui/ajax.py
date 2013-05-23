# -*- coding: UTF-8 -*-
'''
Created on 2013-03-25

@author: tianwei

Desc: This module will be used for ajax request, such as form valid, search
      query, calculated submit.
'''

import simplejson
from dajaxice.decorators import dajaxice_register

from backend.logging import logger
from backend.ChemSpiderPy.wrapper import search_cheminfo


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

    logger.info(unique_names)
    logger.info(smile)
    logger.info(notes)
    logger.info(name)
    logger.info(mol)
    logger.info(types)
    logger.info(models)

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
