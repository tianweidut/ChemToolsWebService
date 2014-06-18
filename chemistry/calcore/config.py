# coding: utf-8

from os.path import dirname, abspath, join
from collections import namedtuple

CONFIG_DIR = dirname(abspath(__file__))
CALCORE_DIR = dirname(CONFIG_DIR)
GAUSSIAN_DATA_PATH = join(CONFIG_DIR, 'forgaussian')
DRAGON_PATH = join(CALCORE_DIR, 'fordragon')
MOPAC_PATH = join(CALCORE_DIR, 'formopac')
GAUSSIAN_PATH = join(CALCORE_DIR, 'forgaussian')
TESTDATA_PATH = join(CALCORE_DIR, 'tests', 'data')

CALCULATE_SOFTWARE_TYPE = namedtuple("CALCULATE_SOFTWARE_TYPE",
        ['DRAGON', 'MOPAC', 'GAUSSIAN'])('DRAGON', 'MOPAC', 'GAUSSIAN')

# 计算软件对应的外部命令，可能根据实际进行修改
CALCULATE_CMD_TYPE = namedtuple("CALCULATE_CMD_TYPE",
        ['DRAGON', 'MOPAC', 'GAUSSIAN'])('dragon6shell -s ', 'mopac ', 'g09 ')

CALCULATE_DATA_PATH = namedtuple('CALCULATE_DATA_PATH',
        ['DRAGON', 'MOPAC', 'GAUSSIAN'])(DRAGON_PATH, MOPAC_PATH, GAUSSIAN_PATH)
