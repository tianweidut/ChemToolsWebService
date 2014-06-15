# coding: utf-8
import os
from os.path import join, exists
import subprocess
import shutil
import pybel
from .config import CALCULATE_DATA_PATH
from .mopac import MopacModel
from .gaussian_optimize import GaussianOptimizeModel
from utils import chemistry_logger
from django.conf.settings import MOL_ABSTRACT_FILE_PATH


class Converter():
    def __init__(self, smiles=None, molfiles=None, modeltype=None):
        self.__invalid_smile = []
        self.__smilenum_list = []
        self.__molfile = []
        self.modeltype = modeltype

        # smiles 可以传入list，也可以传入以comma作为分隔符的smiles字符串
        if isinstance(smiles, list):
            self.__smilenum_list = [s for s in smiles]
        elif isinstance(smiles, basestring):
            self.__smilenum_list = smiles.split(',')

        # molfies 传递的地址是完整路径
        if isinstance(molfiles, list):
            self.__molfile = [f for f in molfiles]
        elif isinstance(molfiles, basestring):
            self.__molfile = molfiles.split(',')

    def smile2_3d(self, smile):
        mymol = pybel.readstring('smi', smile)
        if self.modeltype == 3:
            mymol.addh()
        mymol.make3D()
        name = self.format_filename(smile)
        mol_fpath = join(MOL_ABSTRACT_FILE_PATH, '%s.mol' % name)
        mymol.write('mol', mol_fpath, overwrite=True)
        return mol_fpath

    def iter_smiles_files(self, src_list, src_type):
        for element in src_list:
            if src_type == 'smile':
                name = self.format_filename(element)
            elif src_type == 'file':
                name = os.path.basename(element).split('.')[0]
            else:
                raise Exception('No support %s' % src_type)

            dragon_dpath = join(CALCULATE_DATA_PATH.DRAGON, name)
            mopac_dpath = join(CALCULATE_DATA_PATH.MOPAC, name)
            mop_fpath = join(mopac_dpath, '%s.mop' % name)

            if not os.path.exists(dragon_dpath):
                os.makedirs(dragon_dpath)

            if not exists(mopac_dpath):
                os.makedirs(mopac_dpath)

            yield (element, name, dragon_dpath, mopac_dpath, mop_fpath)

    def mol2dragon_folder(self):
        mop_fname_set = set()

        for element in self.iter_smiles_files(self.__smilenum_list, 'smile'):
            smile, name, dragon_dpath, mopac_dpath, mop_fpath = element
            mol_fpath = join(MOL_ABSTRACT_FILE_PATH, '%s.mol' % name)
            try:
                # '-:smi' 可以直接对smile进行转化
                cmd = 'obabel -:"%s" -o mop -O "%s" --gen3D' % (smile,
                                                                mop_fpath)
                chemistry_logger.debug('mop2mopac, smi->mop: %s' % cmd)
                subprocess.Popen(cmd, shell=True).wait()
            except:
                self.__invalid_smile.append(smile)
                continue

            # 修改smi->mop文件的头部
            lines = []
            with open(mop_fpath, 'rb') as f:
                lines = f.readlines()
                lines[0] = 'EF GNORM=0.0001 MMOK GEO-OK PM3\n'
                lines[1] = mopac_dpath + "\n"

            with open(mop_fpath, 'wb') as f:
                f.writelines(lines)

            shutil.copy(mol_fpath, dragon_dpath)
            mop_fname_set.add('%s.mop' % name)

        for element in self.iter_smiles_files(self.__molfile, 'file'):
            mol_fpath, name, dragon_dpath, mopac_dpath, mop_fpath = element

            shutil.move(mol_fpath, dragon_dpath)
            shutil.move(mop_fpath, dragon_dpath)
            mop_fname_set.add('%s.mop' % name)

        # 使用mopac对dragon结果进行优化
        try:
            mop = MopacModel(mop_fname_set)
            mop.opt4dragon()
        except Exception:
            chemistry_logger.exception('Failed to mopac optimize for dragon')

    def mol2gjf2dragon_folder(self):
        gaussian_files_set = set()

        for element in self.iter_smiles_files(self.__smilenum_list, 'smile'):
            smile, name, dragon_dpath, mopac_dpath, mop_fpath = element
            gaussian_dpath = join(CALCULATE_DATA_PATH.GAUSSIAN, name)

            # smile-> mol
            try:
                mol_fpath = self.smile2_3d(smile)
            except Exception:
                self.__invalid_smile.append(smile)
                chemistry_logger.exception('Failed to convert smile %s to 3D structure' % smile)
                continue

            # mol -> gjf file
            gjf_fpath = mol2gjf(mol_fpath, self.modeltype)

            shutil.copy(mol_fpath, dragon_dpath)
            shutil.copy(gjf_fpath, gaussian_dpath)
            gaussian_files_set.add('%s.gjf' % name)

        for element in self.iter_smiles_files(self.__molfile, 'file'):
            mol_fpath, name, dragon_dpath, mopac_dpath, mop_fpath = element

            shutil.move(mol_fpath, dragon_dpath)
            gaussian_files_set.add('%s.gjf' % name)

        try:
            gjf = GaussianOptimizeModel(gaussian_files_set)
            gjf.gjf4dragon()
        except Exception:
            chemistry_logger.exception('Failed to gaussian optimize for dragon')

    def format_filename(self, filename):
        return filename.replace('\\', '#').replace('/', '$')

    def get_invalid_smile(self):
        return self.__invalid_smile

    def get_smilenum_list(self):
        return self.__smilenum_list

    def get_molfile(self):
        return self.__molfile


def mol2mop(fpath):
    fname = os.path.basename(fpath)
    fname_no_ext = fname.split('.')[0]
    content = []
    with open(fpath, 'f') as f:
        for line in f.readlines():
            try:
                values = line.split()
                if 'A' < values[3] < 'Z':
                    content.append(' %s %s %s %s\n' % (values[3], values[0],
                                                        values[1], values[2]))
            except Exception:
                chemistry_logger.exception('failed to resolve mol2mop line: %s' % line)

    mop_list = []
    mop_list.append('EF GNORM=0.0001 MMOK GEO-OK PM3\n')
    mop_list.append('\n\r\n')
    mop_list.extend(content)
    mop_fpath = join(MOL_ABSTRACT_FILE_PATH, '%s.mop' % fname_no_ext)

    # FIXME：多个人同时写一个名的文件会存在问题
    with open(mop_fpath, 'w') as f:
        f.writelines(tuple(mop_list))

    return mop_fpath


def mol2gjf(fpath, modeltype):
    if modeltype == 3:
        element = dict.fromkeys([
            'H', 'C', 'N', 'O', 'F', 'P', 'S', 'Cl',
            'Se', 'Br', 'I', 'Si', 'Hg', 'Pb'], 0)

    fname = os.path.basename(fpath)
    fname_no_ext = fname.split('.')[0]

    content = []

    with open(fpath, 'r') as f:
        for line in f.readlines():
            try:
                values = line.split()
                if 'A' < values[3] < 'Z':
                    content.append(' %s %s %s %s\n' % (values[3], values[0],
                                                       values[1], values[2]))
                    if modeltype == 3:
                        element[values[3]] = 1

            except Exception:
                chemistry_logger.exception('failed to resolve mol2gjf line: %s' % line)

    gjf_list = []
    gjf_list.append('%chk=%s.chk\n' % fname_no_ext)
    gjf_list.append('%nproc=2\n')
    gjf_list.append('%mem=2GB\n')

    if modeltype == 3:
        element_op = (element['I'] | element['Si'] | element['Hg'] |
                      element['Pb']) == 1
        if element_op:
            gjf_list.append('#p opt freq b3lyp/genecp scf=tight int=ultrafine\n')
        else:
            gjf_list.append('#p opt freq b3lyp/6-311+G(d,p) scf=tight int=ultrafine\n')
    elif modeltype == 2:
        gjf_list.append('#p opt freq b3lyp/6-31+g(d,p) SCRF=(IEFPCM,SOLVENT=WATER)\n')

    gjf_list.append('\n')
    gjf_list.append('Title Card Required\n')
    gjf_list.append('\n')
    gjf_list.append('0 1\n')
    gjf_list.extend(content)
    gjf_list.append('\n')

    if modeltype == 3 and element_op:
        tempC = ""
        tempHg = ""
        for t in ('I', 'Si', 'Hg', 'Pb'):
            if element[t] == 1:
                element[t] = 0
                tempHg += "%s " % t

        for key in element:
            if element[key] == 1:
                tempC += "%s " % key

        gjf_list.append('%s 0\n' % tempC)
        gjf_list.append('6-31+g(d,p)\n')
        gjf_list.append('****\n')
        gjf_list.append('%s 0\n' % tempHg)
        gjf_list.append('LANL2DZ\n')
        gjf_list.append('****\n\n')
        gjf_list.append('%s 0\n' % tempHg)
        gjf_list.append('LANL2DZ\n\n')

    gjf_fpath = join(MOL_ABSTRACT_FILE_PATH, '%s.gjf' % fname_no_ext)
    with open(gjf_fpath, 'w') as f:
        f.writelines(tuple(gjf_list))

    return gjf_fpath
