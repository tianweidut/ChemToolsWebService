# -*- coding: UTF-8 -*-
'''
Created on 2012-11-17

@author: tianwei
'''
import os
from django.conf import settings
from backend.logging import logger

def receiveFile(uploadFileObj):
        """
        upload File objects generate
        """
        try:
            for key,fileop in uploadFileObj.items():
                path = os.path.join(settings.TMP_FILE_PATH ,fileop.name)
                dest = open(path.encode('utf-8'), 'wb+')
                if fileop.multiple_chunks:
                    for c in fileop.chunks():
                        dest.write(c)
                else:
                    dest.write(fileop.read())
                dest.close()
                
            return path
                        
        except Exception,err:
            import pdb;
            print pdb.traceback
            logger.error("recv Error %s "%err)