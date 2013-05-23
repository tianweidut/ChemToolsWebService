#!usr/bin/env python
# coding: utf-8
import subprocess
import re
from calcore.config.settings import  globalpath
from calcore.controllers.PathInit import ParseInitPath
from calcore.controllers.SmileToMol import SmileToMol
from calcore.controllers.XmlCreate import write_xml
#调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC
class Dragon(SmileToMol):
    def __init__(self, smiles_str=None, molfile=None):
        sm = SmileToMol(smiles_str, molfile)
        sm.mol2dragon_folder()
        self.__file = sm.get_smilenum_list()
        for mol in sm.get_molfile():
            self.__file.append(mol.split('.')[0])
        self.invalidnums = sm.get_invalid_smile()
        self.parse=ParseInitPath(globalpath+'config/InitPath.xml')
        #dragon的filepath是xmlCreate生成的xml路径，默认在此文件夹中
        self.OrderPath=self.parse.get_xml_data(globalpath+'config/InitPath.xml','DRAGON')  

    def mol2drs(self):
        for file in self.__file:
                                ########################################################################################
            #if there exists '\' or '/' in filename ,substitute them with '#' and '$'
            regex1 = "\\"
            regex2 = '/'
            
            revisedfilename = ""
            for i in range(0, len(file)):
                if file[i] == regex1:
                    revisedfilename +=  "#"
                elif file[i] == regex2:
                    revisedfilename += "$"
                else:
                    revisedfilename += file[i]
                                ########################################################################################
            filepath = globalpath+"fordragon/"+revisedfilename+"/"
            filename = revisedfilename+".mol"
            wx=write_xml()
            wx.set_tag(filepath+filename, filepath+revisedfilename+'.drs')
            #dragon6shell -s .drs to get the result 
            Cmd=self.OrderPath+"'"+filepath+revisedfilename+".drs'"
            subprocess.Popen(Cmd,shell=True).wait()
    def extractparameter(self,parameters = None):
        '''
        parameters is a list that needs abstracting from drs file
        and method returns a dictionay that has keys that are parameters and values that is value from drs file 
        '''
        firsttraverse = True
        para_dic = {}
        # record para position in drs file
        temp_dic = {}
        for file in self.__file:
                ########################################################################################
            #if there exists '\' or '/' in filename ,substitute them with '#' and '$'
            regex1 = "\\"
            regex2 = '/'
            
            revisedfilename = ""
            for i in range(0, len(file)):
                if file[i] == regex1:
                    revisedfilename +=  "#"
                elif file[i] == regex2:
                    revisedfilename += "$"
                else:
                    revisedfilename += file[i]
                                ########################################################################################
            para_dic[file] = {}
            filepath = globalpath+"fordragon/"+revisedfilename+"/"
            with open(filepath+revisedfilename+'.drs','r') as fp:
                lines = fp.readlines()
                fp.close()
                paraline = lines[0].split()
                valueline = lines[1].split() 
                
            for para in parameters:
                para_dic[file][para] = 0
                
            if firsttraverse:
                firsttraverse = False
                for i in range(len(paraline)):
                    if para_dic[file].has_key(paraline[i]):
                        temp_dic[paraline[i]] = i
                        para_dic[file][paraline[i]] = valueline[i]
            else:
                for key in temp_dic.keys():
                    try:
                        para_dic[file][key] = valueline[temp_dic[key]]
                    except:
                        print key,temp_dic[i],valueline[temp_dic[key]]

                    
                    
        return para_dic



    
