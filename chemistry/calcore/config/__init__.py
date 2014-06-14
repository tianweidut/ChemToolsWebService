# coding: utf-8

from os.path import dirname, abspath, join
from collections import namedtuple

CONFIG_DIR = dirname(abspath(__file__))
globalpath = dirname(CONFIG_DIR)
GAUSSIAN_DATA_PATH = join(CONFIG_DIR, 'forgaussian')
DRAGON_PATH = join(globalpath, 'fordragon')
MOPAC_PATH = join(globalpath, 'formopac')
GAUSSIAN_PATH = join(globalpath, 'forgaussian')
TESTDATA_PATH = join(globalpath, 'tests', 'data')

CALCULATE_SOFTWARE_TYPE = namedtuple("CALCULATE_SOFTWARE_TYPE",
        ['DRAGON', 'MOPAC', 'GAUSSIAN'])('DRAGON', 'MOPAC', 'GAUSSIAN')

# 计算软件对应的外部命令，可能根据实际进行修改
CALCULATE_CMD_TYPE = namedtuple("CALCULATE_CMD_TYPE",
        ['DRAGON', 'MOPAC', 'GAUSSIAN'])('dragon6shell -s ', 'mopac ', 'g09 ')

CALCULATE_DATA_PATH = namedtuple('CALCULATE_DATA_PATH',
        ['DRAGON', 'MOPAC', 'GAUSSIAN'])(DRAGON_PATH, MOPAC_PATH, GAUSSIAN_PATH)
