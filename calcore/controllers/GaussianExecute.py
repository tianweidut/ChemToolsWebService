#! /usr/bin/env python
#coding=utf-8
from controllers.XmlCreate import write_xml
from controllers.CmdChoice import CmdChoice
import threading
import subprocess
import time
from Gaussian import Gaussian
def GuassianDisposal(GuassianFile):
    
    c = Gaussian(GuassianFile)   
    global InputExceptionFlag
    if c.InputExceptionFlag == True:
        print "please check your input validity"
        return 
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

t1 = threading.Thread(target=GuassianDisposal, args=('WaterSolSP.gjf',))
t1.start()  