# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: sytmac
'''

import subprocess
from calcore.controllers.PathInit import ParseInitPath
from calcore.config.settings import globalpath

#调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC
class CmdChoice():
    togo=0;
    def __init__(self):
            self.parse=ParseInitPath(globalpath+'InitPath.xml')
    #得到各个分子计算符软件的路径,进行命令行操作               
    def PathChoiceAndExecute(self,cmd,filePath):
        self.InputFilepath=filePath #public variable
        #dragon的filepath是xmlCreate生成的xml路径，默认在此文件夹中
        if cmd=='DRAGON':
            self.PATH=self.parse.get_xml_data(globalpath+'InitPath.xml''InitPath.xml','DRAGON')
                                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
            Cmd=self.PATH+filePath
            subprocess.Popen(Cmd,shell=True)
            #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
           
        if cmd=='MOPAC':
            self.PATH=self.parse.get_xml_data(globalpath+'InitPath.xml','MOPAC')
                                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
            Cmd=self.PATH+filePath
            subprocess.Popen(Cmd,shell=True)
            #进入针对xml解析的计算分子描述符原始文件的路径,进行计算

        if cmd=='GAUSSIAN':
            self.PATH=self.parse.get_xml_data(globalpath+'InitPath.xml','GAUSSIAN')
                                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
            Cmd=self.PATH+filePath
            subprocess.Popen(Cmd,shell=True)
            


