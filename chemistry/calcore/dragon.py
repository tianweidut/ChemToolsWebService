# coding: utf-8
from os.path import join, basename
import subprocess
import re
from .config import CALCULATE_CMD_TYPE, CALCULATE_DATA_PATH
from .xml_utils import XMLWriter
from .converters import Converter
from utils import chemistry_logger


# 调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC
class DragonModel():

    def __init__(self, model_name, smile=None, molfile=None):
        self.model_name = model_name

        converter = Converter(smile, molfile, self.model_name)
        #FIXME: 使用常量
        if self.model_name in ('logKOA', 'logRP', 'logPL', 'logBDG'):
            converter.mol2dragon_folder()
        elif self.model_name in ('logKOC', 'logBCF', 'logKOH', 'logKOH_T'):
            converter.mol2gjf2dragon_folder()

        self.invalidnums = converter.get_invalid_smile()
        self.names_set = set(i for i in converter.get_smilenum_list())
        # get_molfile 返回的是文件绝对路径列表
        for fpath in converter.get_molfile():
            name = basename(fpath).split('.')[0]
            self.names_set.add(name)

    def format_filename(self, name):
        return name.replace('\\', '#').replace('/', '$')

    def iter_files(self):
        for raw_name in self.names_set:
            fname = self.format_filename(raw_name)
            fpath = join(CALCULATE_DATA_PATH.DRAGON, fname)
            fname_mol = fname + ".mol"
            fname_drs = fname + ".drs"
            input_fpath = join(fpath, fname_mol)
            output_fpath = join(fpath, fname_drs)
            yield raw_name, fname, input_fpath, output_fpath

    def mol2drs(self):
        for raw_name, fname, input_fpath, output_fpath in self.iter_files():
            XMLWriter(input_fpath, output_fpath)
            # dragon6shell -s *.drs to get the result
            cmd = "%s '%s'" % (CALCULATE_CMD_TYPE.DRAGON, output_fpath)
            chemistry_logger.info('mol2drs cmd %s' % cmd)
            subprocess.Popen(cmd, shell=True).wait()

    def extractparameter(self, parameters=None):
        '''从drs文件中将对应参数名列表中对应的描述符名称的值提取出来，返回的是一个字典'''
        firsttraverse = True
        para_dic = {}
        # record para position in drs file
        temp_dic = {}

        for raw_name, fname, input_fpath, output_fpath in self.iter_files():
            para_dic[raw_name] = {p: 0 for p in parameters}
            with open(output_fpath, 'r') as fp:
                lines = fp.readlines()
                paraline = lines[0].split()
                valueline = lines[1].split()

            if firsttraverse:
                firsttraverse = False
                for i in range(len(paraline)):
                    if paraline[i] in para_dic[raw_name]:
                        temp_dic[paraline[i]] = i
                        para_dic[raw_name][paraline[i]] = float(valueline[i])
            else:
                for key in temp_dic.keys():
                    try:
                        para_dic[raw_name][key] = float(valueline[temp_dic[key]])
                    except:
                        print key, temp_dic[i], valueline[temp_dic[key]]

            if self.model_name in ('logKOH', 'logKOH_T'):
                f_log = join(CALCULATE_DATA_PATH.GAUSSIAN, raw_name,
                             '%s.log' % raw_name)
                f = open(f_log, 'r')
                lines = f.readlines()
                f.close()

                regex = '.*Alpha  occ. eigenvalues.*'

                for lineNum in range(len(lines)):
                    if re.match(regex, lines[lineNum]):
                        while(re.match(regex, lines[lineNum])):
                            lineNum = lineNum + 1
                        List = list(lines[lineNum].split(' '))
                        while(1):
                            try:
                                List.remove('')
                            except:
                                break
                        EHOMO = lines[lineNum - 1].split(' ')[-1]
                        para_dic[raw_name]["EHOMO"] = float(EHOMO)
                        break
            elif self.model_name in ('logPL',):
                f_out = join(CALCULATE_DATA_PATH.MOPAC, raw_name,
                             '%.out' % raw_name)
                f = open(f_out, 'r')
                lines = f.readlines()
                f.close()

                regex = '.*ATOM NO\..*TYPE.*CHARGE.*No\.'
                j = 1
                for lineNum in range(len(lines)):
                    if re.match(regex, lines[lineNum]):
                        while(not re.match('.*DIPOLE.*', lines[lineNum])):
                            List = lines[lineNum+j].split()
                            while(1):
                                try:
                                    List.remove('')
                                except:
                                    break
                            j = j + 1
                        para_dic[raw_name]["u"] = lines[lineNum+j+3].split()[-1]
                        break

        return para_dic
