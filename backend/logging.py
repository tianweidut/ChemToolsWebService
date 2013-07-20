# -*- coding: UTF-8 -*-
'''
Created on 2012-11-17

@author: tianwei
'''
#TODO Singleton for logging

from django.utils.log import getLogger

logger = getLogger('django')


def loginfo(p="", label=""):
    logger.info("***"*10)
    logger.info(label)
    logger.info(p)
    logger.info("---"*10)
