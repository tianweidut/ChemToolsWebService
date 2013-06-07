# -* -coding: utf-8 -*- 
'''
Created on 2012-11-26

@author: songyang
'''
import sys, os, shutil, re
sys.path.append("/usr/local/lib/")
import openbabel,pybel
from calcore.config.settings import globalpath
from calcore.controllers.Mopac import Mopac
from calcore.controllers.MolToGjfAndMop import Mol2GjfandMop

class SmileToMol():
    '''
    to transfer from smile numbers to mol file:
    input parameter is a string,and multi_smiles is splited by ','
    such as [number1,number2,number3]
'''
    def __init__(self, smilenum=None, molfile=None,molpath={}):
        self.__invalid_smile  = []
        self.__opt_smilenum   = []
        self.__unopt_smilenum = []
        self.__smilenum_list  = []
        self.__molfile        = []
        self.molpath=molpath
        if smilenum == "":
            #raise Exception,"error input with 0 valid smilenum"
            pass
        else:
            self.__smilenum_list = smilenum.split(',')
        if molfile =="":
            pass
        else:
            self.__molfile = molfile.split(',')
        #for test
        for smilenum in self.__smilenum_list:
            self.__unopt_smilenum.append(smilenum)
        self.__smilenum_list = self.__unopt_smilenum
    def check_smilenum(self): 
            #for query in mysql;
            #if smilenum in database,it means that the mol file has been optimized
            #or we need optimize the mol file with mopac 
            #we use self.__opt_smilenum and self.__unopt_smilenum to mark off optimized or unoptimized mol file
            #using the following code
            
            #for smilenum in self.smilenum_list:
            #    try: 
            #        models.objects.get(smile=smilenum)
            #        self.opt_smilnum.append(smilenum)
            #    exception DoesNotExist:
            #        self.unopt_smilnum.append(smilenum)
            pass
    def smile2_3d(self,smilenum):
            mymol=pybel.readstring('smi',smilenum)
            mymol.addh()
            mymol.make3D()
                        ########################################################################################
            #if there exists '\' or '/' in filename ,substitute them with '#' and '$'
            regex1 = "\\"
            regex2 = '/'
            
            revisedsmi = ""
            for i in range(0, len(smilenum)):
                if smilenum[i] == regex1:
                    revisedsmi +=  "#"
                elif smilenum[i] == regex2:
                    revisedsmi += "$"
                else:
                    revisedsmi += smilenum[i]
            ########################################################################################
            mymol.write('mol',revisedsmi+".mol",overwrite=True)
            
    def mop2mopac_folder(self):
        ######################################################################################
        # deal with smile numbers
        for smilenum in self.__unopt_smilenum:
            #1:smile number to 3d structure
            try:
                self.smile2_3d(smilenum)
            except:
                self.__invalid_smile.append(smilenum)
                continue
            ########################################################################################
            #if there exists '\' or '/' in filename ,substitute them with '#' and '$'
            regex1 = "\\"
            regex2 = '/'
            
            revisedsmi = ""
            for i in range(0, len(smilenum)):
                if smilenum[i] == regex1:
                    revisedsmi +=  "#"
                elif smilenum[i] == regex2:
                    revisedsmi += "$"
                else:
                    revisedsmi += smilenum[i]
            ########################################################################################
            #2:mol to mop file
            Mol2GjfandMop(self.molpath+'/'+revisedsmi+'.mol',mop=True)
            #3:mop file into formopac folder
            dst = globalpath+'formopac/'+revisedsmi
            if not os.path.exists(dst):
                os.makedirs(dst)
            real_dst = os.path.join(dst, revisedsmi+'.mop')
            if os.path.exists(real_dst):
                os.remove(self.molpath+'/'+revisedsmi+'.mop')
            else:
                shutil.move(self.molpath+'/'+revisedsmi+'.mop',globalpath+'formopac/'+revisedsmi)
        # to remove invalide smilenum from self.__unopt_smilenum
        for num in self.__invalid_smile:
            self.__unopt_smilenum.remove(num) 
            ##########################################################################################
            #######################################################################################
        #deal with input mol file
        for mol in self.__molfile:
            Mol2GjfandMop(self.molpath+'/'+mol,mop=True)
            mol_without_ext = mol.split('.')[0]
            dst = globalpath+'formopac/'+mol_without_ext
            if not os.path.exists(dst):
                os.makedirs(dst)
            real_dst = os.path.join(dst, mol_without_ext+'.mop')
            if os.path.exists(real_dst):
                os.remove(self.molpath+'/'+mol_without_ext+'.mop')
            else:
                shutil.move(self.molpath+'/'+mol_without_ext+'.mop',globalpath+'formopac/'+mol_without_ext)
                #######################################################################################
    def mol2dragon_folder(self):
        # mol2mopac_folder here is to put mop file into mopac folder
        # so as to  optimize mol file with Mopac
        self.mop2mopac_folder()
        mopfile = []
        for smilenum in self.__smilenum_list:
                                ########################################################################################
            #if there exists '\' or '/' in filename ,substitute them with '#' and '$'
            regex1 = "\\"
            regex2 = '/'
            
            revisedsmi = ""
            for i in range(0, len(smilenum)):
                if smilenum[i] == regex1:
                    revisedsmi +=  "#"
                elif smilenum[i] == regex2:
                    revisedsmi += "$"
                else:
                    revisedsmi += smilenum[i]
                                ########################################################################################
            #delete mol file in current folder and move it to dragon dictionary
            dst = globalpath+'fordragon/'+revisedsmi+'/'
            if not os.path.exists(dst):
                os.makedirs(dst)
            if not os.path.exists(dst+revisedsmi+'.mol'):
                shutil.move(self.molpath+'/'+revisedsmi+'.mol',dst)
            mopfile.append(revisedsmi+'.mop')
            ###################################################################################
        for mol in self.__molfile:
            mol_without_ext = mol.split('.')[0]
            #delete mol file in current folder and move it to dragon dictionary
            dst = globalpath+'fordragon/'+mol_without_ext+'/'
            if not os.path.exists(dst):
                os.makedirs(dst)
            if not os.path.exists(dst+mol):
                shutil.move(self.molpath+'/'+mol,dst)
            mopfile.append(mol_without_ext+'.mop')
        mop = Mopac(mopfile)
        mop.opt4dragon()
    def get_unopt_smilelist(self):
        return self.__unopt_smilenum
    def get_opt_smilelist(self):
        return self.__opt_smilenum
    def get_invalid_smile(self):
        return self.__invalid_smile
    def get_smilenum_list(self):
        return self.__smilenum_list
    def get_molfile(self):
        return self.__molfile
'''
sm = SmileToMol('cab,cc,cd,ce,ccc')
sm.optimize_mol()
sm.mol2tdragon_dictionary()
print sm.get_invalid_smile()
print sm.get_smilenum_list()
'''
