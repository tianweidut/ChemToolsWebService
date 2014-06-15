# coding: utf-8
import subprocess
import shutil
import os
from os.path import join, exists
from .config import CALCULATE_CMD_TYPE, CALCULATE_DATA_PATH
from utils import chemistry_logger


class GaussianOptimizeModel():
    '''Optimize .gjf --> .log --> .mol'''
    def __init__(self, gjf_fname_list):
        self.gjf_fname_list_no_ext = []

        for fname in gjf_fname_list:
            name = fname.split('.')[0]
            self.gjf_fname_list_no_ext.append(name)

            dpath = join(CALCULATE_DATA_PATH.GAUSSIAN, name)

            if not exists(dpath):
                os.mkdir(dpath)

            try:
                shutil.move(fname, join(dpath, fname))
            except Exception:
                chemistry_logger.exception('Failed to shutil %s' % fname)

    def gjf4dragon(self):
        for name in self.gjf_fname_list_no_ext:
            mol_path = join(CALCULATE_DATA_PATH.DRAGON, name,
                            '%s.mol' % name)
            gjf_path = join(CALCULATE_DATA_PATH.GAUSSIAN, name,
                            '%s.gjf' % name)
            log_path = join(CALCULATE_DATA_PATH.GAUSSIAN, name,
                            '%s.log' % name)

            cmd = '%s "%s"' % (CALCULATE_CMD_TYPE.GAUSSIAN, gjf_path)
            chemistry_logger.debug('gif4dragon part2 cmd: %s' % cmd)
            subprocess.Popen(cmd, shell=True).wait()

            cmd = 'obabel -ig09 "%s" -omol -O "%s"' % (log_path, mol_path)
            chemistry_logger.debug('gif4dragon part2 cmd: %s' % cmd)
            subprocess.Popen(cmd, shell=True).wait()
