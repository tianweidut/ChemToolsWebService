# coding: utf-8
import os
import shutil
import pybel
from chemistry.calcore.config import globalpath
from .Mopac import Mopac
from .GaussianOptimize import *


class SmileToMol():

    '''
    to transfer from smile numbers to mol file:
    input parameter is a string,and multi_smiles is splited by ','
    such as [number1,number2,number3]
    '''

    def __init__(self, smilenum=None, molfile=None,
                 modeltype=None):

        print "in the SmileToMol-init"
        self.__invalid_smile = []
        self.__opt_smilenum = []
        self.__unopt_smilenum = []
        self.__smilenum_list = []
        self.__molfile = []
        self.modeltype = modeltype
        self.molpath = os.path.dirname(molfile)
        self.molusemopac = True
        if smilenum == "":
            #raise Exception,"error input with 0 valid smilenum"
            pass
        else:
            self.__smilenum_list = smilenum.split(',')
        if molfile == "":
            pass
        else:
            self.__molfile = molfile.split(',')
        # for test
        for smilenum in self.__smilenum_list:
            self.__unopt_smilenum.append(smilenum)
        self.__smilenum_list = self.__unopt_smilenum
        print "end SmileToMol-init"

    def smile2_3d(self, smilenum):
        print "in SmileToMol-smile2_3d "
        mymol = pybel.readstring('smi', smilenum)
        if self.modeltype == 3:
            mymol.addh()
        mymol.make3D()
        revisedsmi = self.format_filename(smilenum)
        tmpstring = self.molpath.encode('utf-8') + '/' + revisedsmi + '.mol'
        mymol.write('mol', tmpstring, overwrite=True)
        print "end SmileToMol-smile2_3d"

    def mop2mopac_folder(self):
        # deal with smile numbers
        print "in the SmileToMol-mop2mopac_folder"
        for smilenum in self.__unopt_smilenum:
            # 1:smile number to mop
            revisedsmi = self.format_filename(smilenum)
            dst = globalpath + 'formopac/' + revisedsmi
            if not os.path.exists(dst):
                os.makedirs(dst)
            real_dst = os.path.join(dst, revisedsmi + '.mop')
            print real_dst
            if os.path.exists(real_dst):
                os.remove(real_dst)
            else:
                print "old mop file deleted"
            try:
                cmd = 'obabel -:\"' + smilenum + \
                    '\" -omop -O\"' + real_dst + '\"' + " --gen3D"
                subprocess.Popen(cmd, shell=True).wait()
                print "smi->mop", cmd
            except:
                self.__invalid_smile.append(smilenum)
                print "input smilenum invalide ", smilenum
                continue
            lines = open(real_dst, "rb").readlines()
            lines[0] = 'EF GNORM=0.0001 MMOK GEO-OK PM3\n'
            lines[1] = real_dst + "\n"
            f = open(real_dst, "wb")
            f.writelines(lines)
            f.close()

            print "Mol2GjfandMop-mop close"
            # 3:mop file into formopac folder

        # to remove invalide smilenum from self.__unopt_smilenum
        for num in self.__invalid_smile:
            self.__unopt_smilenum.remove(num)
        # deal with input mol file
        for mol in self.__molfile:
            # molusemopac=False
            if self.molusemopac:
                mol_without_ext = mol.split('.')[0]
                Mol2GjfandMop(self.molpath + '/' + mol, mop=True)
                dst = globalpath + 'formopac/' + mol_without_ext
                if not os.path.exists(dst):
                    os.makedirs(dst)
                real_dst = os.path.join(dst, mol_without_ext + '.mop')
                if os.path.exists(real_dst):
                    os.remove(self.molpath + '/' + mol_without_ext + '.mop')
                else:
                    shutil.move(
                        self.molpath +
                        '/' +
                        mol_without_ext +
                        '.mop',
                        globalpath +
                        'formopac/' +
                        mol_without_ext)
            else:
                mol_without_ext = mol.split('.')[0]
                dst = globalpath + 'fordragon/' + mol_without_ext
                if not os.path.exists(dst):
                    os.makedirs(dst)
                real_dst = os.path.join(self.molpath, mol_without_ext + '.mol')
                if os.path.exists(real_dst):
                    if os.path.exists(dst + '/' + mol_without_ext + '.mol'):
                        self.delete_file_folder(
                            dst +
                            '/' +
                            mol_without_ext +
                            '.mol')
                    shutil.move(
                        self.molpath +
                        '/' +
                        mol_without_ext +
                        '.mol',
                        dst)
                else:
                    raise Exception("molpath have no mol!")
                ###############################################################
        print "end SmileToMol-mop2mopac_folder"

    def gjf2gaussian_folder(self):
        #######################################################################
        # deal with smile numbers
        print "in the SmileToMol-gjf2gaussian_folder"
        print self.__unopt_smilenum
        for smilenum in self.__unopt_smilenum:
            # 1:smile number to 3d structure
            # print smilenum
            try:
                self.smile2_3d(smilenum)
            except:
                self.__invalid_smile.append(smilenum)
                print "input smilenum invalide ", smilenum
                continue

            revisedsmi = self.format_filename(smilenum)

            dst = globalpath + 'forgaussian/' + revisedsmi
            dsd = globalpath + 'fordragon/' + revisedsmi
            if os.path.exists(dst):
                self.delete_file_folder(dst)
            if os.path.exists(dsd):
                self.delete_file_folder(dsd)
            # 2:mol to gjf file
            Mol2GjfandMop(
                self.molpath +
                '/' +
                revisedsmi +
                '.mol',
                self.modeltype,
                gjf=True)
            # 3:mop file into formopac folder

            if not os.path.exists(dst):
                os.makedirs(dst)
            real_dst = os.path.join(dst, revisedsmi + '.gjf')
            print real_dst
            if os.path.exists(real_dst):
                os.remove(self.molpath + '/' + revisedsmi + '.gjf')  # ----添加
                # if os.path.exists(self.molpath+'/'+revisedsmi+'.chk'):
                    # os.remove(self.molpath+'/'+revisedsmi+'.chk')
                # if os.path.exists(self.molpath+'/'+revisedsmi+'.mol'):
                    # os.remove(self.molpath+'/'+revisedsmi+'.mol')
                # os.remove(self.molpath+'/'+revisedsmi+'.chk')
                # os.remove(real_dst)
                # print "remove real_dst"
            else:
                shutil.move(
                    self.molpath +
                    '/' +
                    revisedsmi +
                    '.gjf',
                    globalpath +
                    'forgaussian/' +
                    revisedsmi)
                # if os.path.exists(self.molpath+'/'+revisedsmi+'.chk'):
                    # os.remove(self.molpath+'/'+revisedsmi+'.chk')
        # to remove invalide smilenum from self.__unopt_smilenum
        for num in self.__invalid_smile:
            self.__unopt_smilenum.remove(num)
            ###################################################################
            ###################################################################
        # deal with input mol file
        for mol in self.__molfile:
            # Mol2GjfandMop(self.molpath+'/'+mol,gjf=True)
            mol_without_ext = mol.split('.')[0]
            dst = globalpath + 'fordragon/' + mol_without_ext
            print mol_without_ext
            print dst
            if not os.path.exists(dst):
                os.makedirs(dst)
            real_dst = os.path.join(dst, mol_without_ext + '.mol')
            if os.path.exists(real_dst):
                os.remove(self.molpath + '/' + mol_without_ext + '.mol')
            else:
                shutil.move(
                    self.molpath +
                    '/' +
                    mol_without_ext +
                    '.mol',
                    globalpath +
                    'fordragon/' +
                    mol_without_ext)
            # if os.path.exists(self.molpath+'/'+revisedsmi+'.chk'):
               # os.remove(self.molpath+'/'+revisedsmi+'.chk')
                ###############################################################
        print "end SmileToMol-gjf2gaussian_folder"

    def mol2dragon_folder(self):
        # mol2mopac_folder here is to put mop file into mopac folder
        # so as to  optimize mol file with Mopac
        print "in the mol2dragon_folder"
        self.mop2mopac_folder()
        mopfile = []
        for smilenum in self.__smilenum_list:
            revisedsmi = self.format_filename(smilenum)
            # delete mol file in current folder and move it to dragon
            # dictionary
            dst = globalpath + 'fordragon/' + revisedsmi + '/'
            if not os.path.exists(dst):
                os.makedirs(dst)
            print os.path.exists(self.molpath + '/' + revisedsmi + '.mol')
            if os.path.exists(self.molpath + '/' + revisedsmi + '.mol'):
                shutil.move(self.molpath + '/' + revisedsmi + '.mol', dst)
            mopfile.append(revisedsmi + '.mop')
            ###################################################################
        if self.molusemopac:
            for mol in self.__molfile:
                mol_without_ext = mol.split('.')[0]
                # delete mol file in current folder and move it to dragon
                # dictionary
                dst = globalpath + 'fordragon/' + mol_without_ext + '/'
                if not os.path.exists(dst):
                    os.makedirs(dst)
                if not os.path.exists(dst + mol):
                    shutil.move(self.molpath + '/' + mol, dst)
                mopfile.append(mol_without_ext + '.mop')
        mop = Mopac(mopfile)
        mop.opt4dragon()
        print "end mol2dragon_folder"

    def mol2gjf2dragon_folder(self):
        self.gjf2gaussian_folder()
        gaussianfile = []
        revisedsmi = ""
        for smilenum in self.__smilenum_list:
            revisedsmi = self.format_filename(smilenum)
            # delete mol file in current folder and move it to dragon
            # dictionary
            dst = globalpath + 'fordragon/' + revisedsmi + '/'
            if not os.path.exists(dst):
                os.makedirs(dst)
            if not os.path.exists(dst + revisedsmi + '.mol'):
                shutil.move(self.molpath + '/' + revisedsmi + '.mol', dst)
            gaussianfile.append(revisedsmi + '.gjf')

        if gaussianfile:
            gjf = GaussianOptimize(gaussianfile)
            gjf.gjf4dragon()
        if os.path.exists(self.molpath + '/' + revisedsmi + '.chk'):
            os.remove(self.molpath + '/' + revisedsmi + '.chk')
        print "end mol2gjf2dragon_folder"

    def format_filename(self, filename):
        # if there exists '\' or '/' in filename ,substitute them with '#' and '$'
        return filename.replace('\\', '#').replace('/', '$')

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

    def delete_file_folder(self, src):
        if os.path.isfile(src):
            try:
                os.remove(src)
            except:
                raise Exception('can not delete ' + src)
        elif os.path.isdir(src):
            for item in os.listdir(src):
                itemsrc = os.path.join(src, item)
                self.delete_file_folder(itemsrc)
            try:
                os.rmdir(src)
            except:
                raise Exception('can not delete ' + src)
'''
sm = SmileToMol('cab,cc,cd,ce,ccc')
sm.optimize_mol()
sm.mol2tdragon_dictionary()
print sm.get_invalid_smile()
print sm.get_smilenum_list()
'''


def Mol2GjfandMop(file, modeltype=None,gjf=False, mop=False):
    #to gain input file name such as i.gif
    print "in the Mol2GjfandMop"
    print modeltype
    if modeltype==3:
        element=dict.fromkeys(['H','C','N','O','F','P','S','Cl','Se','Br','I','Si','Hg','Pb'],0)
    #print element
    Inputfilename=file.split('/')[-1]
    #to gain input file name without extension such as i.gif
    InputfilenameWithoutExt=Inputfilename.split('.')[0]
    OritationList=[]
    print file
    f=open(file,'r')
    lines=f.readlines()
    f.close()
    for lineNum in range(0 , len(lines)):
        try:
            List=list(lines[lineNum].split())
            if(List[3]>'A'and List[3]<'Z'):     
                OritationList.append(' '+List[3]+'             '+List[0]+'    '+List[1]+'    '+List[2]+'\n')
                if modeltype==3:
                    element[List[3]]=1
                    #print List[3]
                    #print element[List[3]]
        except:
            continue                                       
    if gjf == True:
        print "gjf=true"
        GjfList=[]   
        GjfList.append('%chk='+InputfilenameWithoutExt+'.chk\n')
        GjfList.append('%nproc=2\n')
        GjfList.append('%mem=2GB\n')
        if modeltype==3:
            if (element['I']|element['Si']|element['Hg']|element['Pb'])==1:
                GjfList.append('#p opt freq b3lyp/genecp scf=tight int=ultrafine\n')
                #print "to do B"
            else:
                GjfList.append('#p opt freq b3lyp/6-311+G(d,p) scf=tight int=ultrafine\n')
        elif modeltype==2:
            GjfList.append('#p opt freq b3lyp/6-31+g(d,p) SCRF=(IEFPCM,SOLVENT=WATER)\n')
        GjfList.append('\n')
        GjfList.append('Title Card Required\n')
        GjfList.append('\n')
        GjfList.append('0 1\n')
        GjfList.extend(OritationList)
        GjfList.append('\n')
        tempC=""
        tempHg=""
        if modeltype==3 and (element['I']|element['Si']|element['Hg']|element['Pb'])==1:
            templist=('I','Si','Hg','Pb')
            for temp in templist:
                if element[temp]==1:
                    tempHg=tempHg+temp+" "
                    element[temp]=0

            for key in element:
                if element[key]==1:
                    tempC=tempC+key+" "
            GjfList.append(tempC+'0\n')
            GjfList.append('6-31+g(d,p)\n')
            GjfList.append('****\n')
            GjfList.append(tempHg+'0\n')
            GjfList.append('LANL2DZ\n')
            GjfList.append('****\n\n')
            GjfList.append(tempHg+'0\n')
            GjfList.append('LANL2DZ\n\n')

        f=open(file.split('.')[0]+'.gjf','w')
        f.writelines(tuple(GjfList))
        f.close()
        print "Mol2GjfandMop-gjf close"
    if mop == True:
        print "mop=True"
        MopList=[]
        MopList.append('EF GNORM=0.0001 MMOK GEO-OK PM3\n')
        #MopList.append('opt freq b3lyp/6-31+g(d,p) SCRF=(IEFPCM,SOLVENT=WATER)\n')
        MopList.append('\n\r\n')
        MopList.extend(OritationList)
        f=open(file.split('.')[0]+'.mop','w')
        f.writelines(tuple(MopList))
        f.close()
        print "Mol2GjfandMop-mop close"
#Mol2GjfandMop('/home/est863/workspace/863program/src/controllers/C(Cl)(Cl)(Cl)C.mol', mop = True)
