# coding: utf-8
from os.path import join
import subprocess
import re
from chemistry.calcore.config import CALCULATE_CMD_TYPE, CALCULATE_DATA_PATH
from .xml_utils import XMLWriter
from .converters import SmileToMol


# 调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC
class Dragon(SmileToMol):

    def __init__(self, model_name, smile=None, molfile=None):
        self.mode_name = model_name
        self.model_type = self.get_model_type(model_name)

        sm = SmileToMol(smile, molfile, self.model_type)

        if self.model_type == 1:
            sm.mol2dragon_folder()
        elif self.model_type == 2 or self.model_type == 3:
            sm.mol2gjf2dragon_folder()

        self.files_list = sm.get_smilenum_list()
        for mol in sm.get_molfile():
            self.files_list.append(mol.split('.')[0])

        self.invalidnums = sm.get_invalid_smile()

    def format_filename(self, name):
        return name.replace('\\', '#').replace('/', '$')

    def iter_files(self):
        for raw_name in self.files_list:
            fname = self.format_filename(raw_name)
            fpath = join(CALCULATE_DATA_PATH.DRAGON, fname)
            fname_mol = fname + ".mol"
            fname_drs = fname + ".drs"
            input_fpath = join(fpath, fname_mol)
            output_fpath = join(fpath, fname_drs)
            yield raw_name, fname, input_fpath, output_fpath

    def get_model_type(self, model_name):
        if model_name in ("logKOA", "logRP"):
            model_type = 1
        elif model_name in ("logKOC", "logBCF"):
            model_type = 2
        elif model_name in ("logKOH", "logKOH_T"):
            model_type = 3
        else:
            model_type = 0

        return model_type

    def mol2drs(self):
        for raw_name, fname, input_fpath, output_fpath in self.iter_files():
            XMLWriter(input_fpath, output_fpath)
            # dragon6shell -s *.drs to get the result
            cmd = "%s '%s'" % (CALCULATE_CMD_TYPE.DRAGON, output_fpath)
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

            if self.modeltype == 3:
                f_log = join(CALCULATE_DATA_PATH.GAUSSIAN, raw_name,
                             raw_name + '.log')
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
        return para_dic
