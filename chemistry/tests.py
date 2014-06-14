#coding: utf-8
import base64
from django.test import TestCase
from django.contrib.auth.models import User
from mock import Mock, patch

from nose.tools import eq_, ok_
from utils import basic_auth_api
from chemistry.util import calculate_tasks


class AuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test1', 'test1@t.com', '123')

    def test_auth_api_user(self):
        request = Mock()
        request.user = self.user
        ok_(basic_auth_api(request))

    def test_auth_api_meta(self):
        request = Mock()
        request_text = base64.encodestring('test1:123')
        request.META = {"HTTP_AUTHORIZATION": "basic %s" % request_text}
        ok_(basic_auth_api(request))

        request = Mock()
        request_text = base64.encodestring('test1:1234')
        request.META = {"HTTP_AUTHORIZATION": "basic %s" % request_text}
        ok_(not basic_auth_api(request))

        request = Mock()
        request_text = base64.encodestring('test123:1234')
        request.META = {"HTTP_AUTHORIZATION": "basic %s" % request_text}
        ok_(not basic_auth_api(request))

    def tearDown(self):
        self.user.delete()


class TaskSubmitTest(TestCase):

    smile = "COc1ccccc1NC(=O)CC(=O)C"
    files_id_list = ['ff2da209-7fd5-4fe4-a398-ee4c3a2a6d68',
                     'b56be350-17dd-4bf4-846e-fce7a5a1a299']
    mol_data = None
    models = [{'model': 'koa', 'temperature': '10'},
              {'model': 'pl', 'temperature': '11'}]
    task_name = "test_task"
    task_notes = "test_notes"

    def setUp(self):
        self.user = User.objects.create_user('test1', 'test1@t.com', '123')

    def tearDown(self):
        self.user.delete()

    def test_submit(self):
        pass

    def test_calculate_task(self):
        num = calculate_tasks(self.files_id_list, self.smile,
                              self.mol_data, self.models)
        eq_(num, 6)

        num = calculate_tasks([], self.smile,
                              self.mol_data, self.models)
        eq_(num, 2)


class PredictionModelTest(TestCase):
    pass
'''
para ={
    "smilestring":"c1ccccc1C(=O)c1cc(c(cc1O)OC)S(=O)(=O)O,c1(ccc(cc1)OC)/C=C/C(=O)OCCOCC",
    "filename"   :"",
    "cas"        :"",
       }
pm = PredictionModel(["logKOA", "logRP"], para)
'''
