# -*- coding:utf-8 -*-
from  xml.dom import  minidom
import os
class ParseInitPath():
    
    def __init__(self,filename):
        self.doc = minidom.parse(filename) 
        self.doc.toxml('UTF-8')
    #得到xml属性值
    def get_attrvalue(self,node, attrname):
        return node.getAttribute(attrname) if node else ''
    #得到节点值
    def get_nodevalue(self,node, index = 0):
        return node.childNodes[index].nodeValue if node else ''
    #得到节点
    def get_xmlnode(self,node,name):
        return node.getElementsByTagName(name) if node else []
    #选择进行计算的原始文件的路径
    def get_xml_data(self,filename,software_call):        
        root = self.doc.documentElement
        if software_call=="DRAGON":
            
            DRAGON = self.get_xmlnode(root,'DRAGON')    
            print DRAGON
            for node in DRAGON: 
                DRAGON_PATH = self.get_xmlnode(node,'PATH')
                print DRAGON_PATH
                DRAGON_PATH_Value=self.get_nodevalue(DRAGON_PATH[0])
            print DRAGON_PATH_Value
            print os.environ[DRAGON_PATH_Value]+'dragon6shell -s '
            return os.environ[DRAGON_PATH_Value]+'dragon6shell -s '  
        elif software_call=="MOPAC":
            MOPAC = self.get_xmlnode(root,'MOPAC')    
            for node in MOPAC:
                MOPAC_PATH = self.get_xmlnode(node,'PATH')
                #print MOPAC_PATH[0]
                MOPAC_PATH_Value=self.get_nodevalue(MOPAC_PATH[0])
            print MOPAC_PATH_Value
            #print os.environ[MOPAC_PATH_Value]
            return MOPAC_PATH_Value
        elif software_call=="GAUSSIAN":
            GAUSSIAN = self.get_xmlnode(root,'GAUSSIAN')    
            for node in GAUSSIAN:
                GAUSSIAN_PATH = self.get_xmlnode(node,'PATH')
                GAUSSIAN_PATH_Value=self.get_nodevalue(GAUSSIAN_PATH[0])
            return GAUSSIAN_PATH_Value
"""
#if __name__ == "__main__":
parse=ParseInitPath('InitPath.xml')
parse.get_xml_data('InitPath.xml','GAUSSIAN')
"""

