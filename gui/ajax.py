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
def calculate_submit(request, data):
    logger.info(data)
    return simplejson.dumps({'message': 'tianwei hello world!'+data})
