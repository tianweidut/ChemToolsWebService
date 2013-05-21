# -*- coding: UTF-8 -*-
'''
Created on 2012-11-17

@author: tianwei
'''
import base64
import simplejson

from django.contrib.auth.models import User

from deps.common.chem.json.message_json import *
from backend.logging import logger
from users.models import UserProfile


class message_handler(object):
    """
        This decorator will deal with decrypting and encrypting the request
        and the response for the api requests received, using the provided key,
        aes_key or figuring the aes_key when agentID is present in the request.
    """
    def __init__(self, message_type, response_type):
        self.message_type = message_type
        self.response_type = response_type

    def __call__(self, method):
        def wrappered_method(handler, request, *args, **kwargs):
            msg = request.POST.get('msg', None)
            msg_recv = self.message_type()
            msg_resp = self.response_type()
            #TODO : We can add RSA algorigthm in recv
            msg_recv.ParseFromString(base64.b64decode(msg))  
            has_obj = True
            try:
                msg_recv.agentID
            except:
                has_obj = False

            #agentID authentication
            if has_obj and msg_recv.agentID is not None and cmp(msg_recv.agentID, "FFFF-FFFF") != 0:
                try:
                    agent = UserProfile.objects.get(agentID=msg_recv.agentID)
                    authentication_pass = True
                except UserProfile.DoesNotExist:
                    authentication_pass = False
                    logger.info("Cannot find this agendID")
            else:
                authentication_pass = False

            response = method(handler,
                              request,
                              msg_recv,
                              msg_resp,
                              authentication_pass=authentication_pass,
                              *args, **kwargs)

            #TODO: We can add RSA algorigthm in resp
            return base64.b64encode(response.SerializeToString())
            #return response.SerializeToString()
        return  wrappered_method


class message_handler_json(object):
    """
        This decorator will deal with decrypting and encrypting the request
        and the response for the api requests received, using the provided key,
        aes_key or figuring the aes_key when agentID is present in the request.
    """
    def __init__(self, message_type, response_type):
        self.message_type = message_type
        self.response_type = response_type

    def ParseFromStringToObject(self, json, message_type):
        dct = simplejson.loads(json, strict=False)
        msg_obj = parseJsonToObject(dct, message_type)
        return msg_obj

    def SerializeToString(self, obj):
        return simplejson.dumps(obj, default=lambda o: o.__dict__)

    def __call__(self, method):
        def wrappered_method(handler, request, *args, **kwargs):
            msg = request.POST.get('msg', None)
            #TODO : We can add RSA algorigthm in recv
            msg_recv = self.ParseFromStringToObject(base64.b64decode(msg), self.message_type)  
            msg_resp = self.response_type()

            has_obj = True
            try:
                msg_recv.agentID
            except:
                has_obj = False
            #agentID authentication
            if has_obj and msg_recv.agentID is not None and cmp(msg_recv.agentID, "FFFF-FFFF") != 0:
                try:
                    agent = UserProfile.objects.get(agentID=msg_recv.agentID)
                    authentication_pass = True
                except UserProfile.DoesNotExist:
                    authentication_pass = False
                    logger.info("Cannot find this agendID")
            else:
                authentication_pass = False

            response = method(handler,
                              request,
                              msg_recv,
                              msg_resp,
                              authentication_pass=authentication_pass,
                              *args, **kwargs)

            #TODO: We can add RSA algorigthm in resp
            return base64.b64encode(self.SerializeToString(response))
        return wrappered_method
