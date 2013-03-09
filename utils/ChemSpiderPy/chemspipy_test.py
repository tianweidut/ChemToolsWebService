# -*- coding: utf-8 -*-
""" Unit tests for chemspipy.py
https://github.com/mcs07/ChemSpiPy

Forked from ChemSpiPy by Cameron Neylon
https://github.com/cameronneylon/ChemSpiPy
"""


import unittest

from chemspipy import *

class TestChemSpiPy(unittest.TestCase):

    def setUp(self):
        self.test_int = 236
        self.test_string = '236'
        self.test_imageurl = 'http://www.chemspider.com/ImagesHandler.ashx?id=236'
        self.test_mf = 'C_{6}H_{6}'
        self.test_smiles = 'c1ccccc1'
        self.test_inchi = 'InChI=1/C6H6/c1-2-4-6-5-3-1/h1-6H'
        self.test_inchikey = 'UHOVQNZJYSORNB-UHFFFAOYAH'
        self.test_averagemass = 78.112
        self.test_molecularweight = 78.1118
        self.test_monoisotopicmass = 78.0469970703125
        self.test_nominalmass = 78
        self.test_alogp = 0
        self.test_xlogp = 0
        self.test_commonname = 'Benzene'

    def test_compound(self):
        """ Unit tests for the Compound class """
        self.assertRaises(TypeError, Compound, 1.2)
        self.assertRaises(TypeError, Compound, 'notadigit')
        self.assertEqual(Compound(self.test_int).csid, self.test_string)
        self.assertEqual(Compound(self.test_string).csid, self.test_string)
        self.assertEqual(Compound(self.test_string).imageurl, self.test_imageurl)
        self.assertEqual(Compound(self.test_string).mf, self.test_mf)
        self.assertEqual(Compound(self.test_string).smiles, self.test_smiles)
        self.assertEqual(Compound(self.test_string).inchi, self.test_inchi)
        self.assertEqual(Compound(self.test_string).inchikey, self.test_inchikey)
        self.assertEqual(Compound(self.test_string).averagemass, self.test_averagemass)
        self.assertEqual(Compound(self.test_string).molecularweight, self.test_molecularweight)
        self.assertEqual(Compound(self.test_string).monoisotopicmass, self.test_monoisotopicmass)
        self.assertEqual(Compound(self.test_string).nominalmass, self.test_nominalmass)
        self.assertEqual(Compound(self.test_string).alogp, self.test_alogp)
        self.assertEqual(Compound(self.test_string).xlogp, self.test_xlogp)
        self.assertEqual(Compound(self.test_string).commonname, self.test_commonname)

    def test_find(self):
        self.assertEqual(find_one('zxbdfgbfgb'), None)
        self.assertEqual(find('zxbdfgbfgb'), None)
        self.assertEqual(find_one(self.test_commonname).csid, self.test_string)
        self.assertEqual(find(self.test_commonname)[0].csid, self.test_string)


if __name__ == '__main__':
    unittest.main()

