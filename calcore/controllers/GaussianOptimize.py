#! /usr/bin/env python
#coding=utf-8
'''
Created on 2013-7-4

@author:sunch
'''
from calcore.config.settings import globalpath
import subprocess
from calcore.controllers.PathInit import ParseInitPath
import shutil
import re
import time
import os

class GaussianOptimize():
    '''
    Optimize .gjf to .log to mol
    '''
    def __init__(self,filename):
        print "in GaussianOptimize-init"
        self.parse = ParseInitPath(globalpath+'config/InitPath.xml')
        self.commandpath=self.parse.get_xml_data(globalpath+'config/InitPath.xml','GAUSSIAN')
        self.filename=filename
        self.filename_without_ext=[]
        self.gjffilepath=[]
        self.gjffilename=[]
        for inputfilename in self.filename:
            filename_without_ext=inputfilename.split('.')[0]
            self.filename_without_ext.append(filename_without_ext)

        try:
            os.mkdir(globalpath+'forgaussian/'+filename_without_ext)
        except:
            print 'can not mkdir in forgaussian'
        gjffilepath=globalpath+'forgaussian/'+filename_without_ext+'/'
        self.gjffilepath.append(gjffilepath)
        try:
            shutil.move(filename,gjffilepath+inputfilename)
        except:
            print "can not move gjffile"
        self.gjffilename.append(filename_without_ext+'.gjf')
        print self.gjffilepath
        print self.filename_without_ext
        print "end GaussianOptimize-init"
        
    def gjf4dragon(self):
        print self.filename
        print len(self.filename)
        for i in range(0,len(self.filename)):
            dragonpath=globalpath+'fordragon/'+self.filename_without_ext[i]+'/'+self.filename_without_ext[i]+'.mol'
            cmd=self.commandpath+"'"+self.gjffilepath[i]+self.filename[i]+"'"
            print "g09 gjf->.log"
            subprocess.Popen(cmd,shell=True).wait()
            print "end g09;.log->mol" 
            cmd='obabel -ig09 '+self.gjffilepath[i]+self.filename_without_ext[i]+'.log '+' -omol -O '+dragonpath
            subprocess.Popen(cmd,shell=True).wait()
            print "end obenbel;mol"

            

