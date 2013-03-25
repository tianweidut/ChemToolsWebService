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

    # Calculated Submit Process
    logger.info(unique_names)
    logger.info(types)

    return simplejson.dumps({'message': 'tianwei hello world!'})
