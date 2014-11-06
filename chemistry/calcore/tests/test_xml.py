# coding: utf-8
import os
from nose.tools import ok_
from django.test import TestCase
from chemistry.calcore.utils import XMLWriter


class XMLWriterTest(TestCase):
    input_fpath = 'xml_writer_inut_path'
    output_fpath = 'xml_writer_output_path.drs'

    def setUp(self):
        if os.path.exists(self.output_fpath):
            os.remove(self.output_fpath)

    def test_writer(self):
        ok_(not os.path.exists(self.output_fpath))
        xm = XMLWriter(self.input_fpath, self.output_fpath)
        xm.display()
        ok_(self.input_fpath in xm.get_content())
        ok_(os.path.exists(self.output_fpath))

    def tearDown(self):
        os.remove(self.output_fpath)
