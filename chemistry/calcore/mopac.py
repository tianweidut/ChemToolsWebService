# coding: utf-8
import subprocess
import shutil
import os
from os.path import join, exists

from .config import CALCULATE_CMD_TYPE, CALCULATE_DATA_PATH
from utils import chemistry_logger


class Mopac():
    def __init__(self, mop_fname_list):
        self.mop_fname_list_no_ext = []

        for fname in mop_fname_list:
            name = fname.split('.')[0]
            self.mop_fname_list_no_ext.append(name)

            dpath = join(CALCULATE_DATA_PATH.MOPAC, name)

            if not exists(dpath):
                os.mkdir(dpath)

            try:
                shutil.move(fname, join(dpath, fname))
            except Exception:
                chemistry_logger.exception('Failed to shutil %s' % fname)

    def opt4dragon(self):
        for name in self.mop_fname_list_no_ext:
            mol_path = join(CALCULATE_DATA_PATH.DRAGON, name,
                            '%s.mol' % name)
            mop_path = join(CALCULATE_DATA_PATH.MOPAC, name,
                            '%s.mop' % name)
            out_path = join(CALCULATE_DATA_PATH.MOPAC, name,
                            '%s.out' % name)

            cmd = '%s "%s"' % (CALCULATE_CMD_TYPE.MOPAC, mop_path)
            chemistry_logger.debug('opt4dragon part1 cmd: %s' % cmd)
            subprocess.Popen(cmd, shell=True).wait()

            # get the optimized orientation in out file and replace counterpart
            # in mol file with it now orientation_info
            # is filed with optimized orientationn

            cmd = 'obabel -imoo "%s" -omol -O "%s" --gen3D' % (out_path,
                                                               mol_path)
            chemistry_logger.debug('opt4dragon part2 cmd: %s' % cmd)
            subprocess.Popen(cmd, shell=True).wait()
