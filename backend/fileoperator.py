# -*- coding: UTF-8 -*-
'''
Created on 2012-11-17

@author: tianwei
'''
import os
from django.conf import settings
from backend.logging import logger

def receiveFile(uploadFileObj, save_path=None):
        """
        upload File objects generate
        """
        try:
            for key, fileop in uploadFileObj.items():
                save_path = save_path if save_path is not None else settings.TMP_FILE_PATH
                path = os.path.join(save_path, fileop.name)
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
