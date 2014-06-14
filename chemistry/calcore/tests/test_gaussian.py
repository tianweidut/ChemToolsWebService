# coding: utf-8
import os
from django.test import TestCase
from nose.tools import eq_, ok_

from chemistry.calcore.controllers.Gaussian import Gaussian
from chemistry.calcore.config import TESTDATA_PATH


class GaussianTest(TestCase):
    def test_run(self):
        return
        test_file = os.path.join(TESTDATA_PATH, 'WaterSolSP.gjf')

        c = Gaussian(test_file)
        if c.InputExceptionFlag:
            raise Exception("please check your input validity")
        else:
            c.GasPhaseParameterCompute()
            c.GasPhase_MolecularVolume()
            c.GasPhase_MolecularHOMOAndLUMOAndAbsolut_Hardness()
            c.Gaussian_electronstaticpotential_chkTofchk()
            c.Gaussian_electronstaticpotential_fckTocub()
            c.GasBindEnergy()
            c.GasPhase_IonizationPotential()
            c.GasPhase_ElectronAffinity()
            c.GasPhase_EnergyProtonation()

            c.Gaussian_electronstaticpotential_output()
            c.Gaussian_electronstaticpotential_parameterCompute()
            c.GasPhase_QmaxAndQmin()
            c.GasPhase_PPCG()
            c.GasPhase_RNGG()
            c.GasPhase_AverageAbsoluteValue()
        print 'Gaussian finished'
