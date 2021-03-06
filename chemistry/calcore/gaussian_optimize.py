# coding: utf-8
from os.path import join
from .config import CALCULATE_CMD_TYPE, CALCULATE_DATA_PATH
from utils import chemistry_logger
from chemistry.calcore.utils import CalcoreCmd


class GaussianOptimizeModel():
    '''Optimize .gjf --> .log --> .mol'''
    def __init__(self, gjf_fname_list):
        self.gjf_fname_list_no_ext = []

        for fname in gjf_fname_list:
            self.gjf_fname_list_no_ext.append(fname.split('.')[0])

    def gjf4dragon(self, model_name):
        for name in self.gjf_fname_list_no_ext:
            mol_path = join(CALCULATE_DATA_PATH.DRAGON, model_name, name,
                            '%s.mol' % name)
            gjf_path = join(CALCULATE_DATA_PATH.GAUSSIAN, model_name, name,
                            '%s.gjf' % name)
            log_path = join(CALCULATE_DATA_PATH.GAUSSIAN, model_name, name,
                            '%s.log' % name)

            cmd = '%s "%s"' % (CALCULATE_CMD_TYPE.GAUSSIAN, gjf_path)
            chemistry_logger.info('gif4dragon part1 cmd: %s' % cmd)
            # 此处需要注意g09输出是.log文件
            CalcoreCmd(cmd, output=log_path).run()

            cmd = 'obabel -ig09 "%s" -omol -O "%s"' % (log_path, mol_path)
            chemistry_logger.info('gif4dragon part2 cmd: %s' % cmd)
            CalcoreCmd(cmd, output=mol_path).run()
