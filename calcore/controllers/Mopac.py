#! /usr/bin/env python
#coding=utf-8
from calcore.config.settings import  globalpath
import subprocess
from calcore.controllers.PathInit import ParseInitPath
import shutil
import re
import time
import os
#调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC
class Mopac():
    '''
    to deal with mop file and get molecular descriptor
    filepath is a list consisting of molfile name  
    '''
    def __init__(self,filename):        
        self.parse = ParseInitPath(globalpath+'config/InitPath.xml')        
        #dragon的filepath是xmlCreate生成的xml路径，默认在此文件夹中
        temppath=os.environ['mopac']
        self.commandpath=temppath+' '
        #self.commandpath = self.parse.get_xml_data(globalpath+'config/InitPath.xml','MOPAC')        
        #self.InputFile=filePath #public variable       
        #to gain input file name such as i.mop it is a list
        self.filename                = filename     
        self.filename_without_ext    = []        
        self.mopfilepath             = []        
        self.mopfilename            = []        
        for inputfilename in self.filename:           
            #to gain input file name without extension such as i
            filename_without_ext = inputfilename.split('.')[0]           
            self.filename_without_ext.append(filename_without_ext) 
                                #####################################################################################################
            #build new dictionary 
            try:                   
                os.mkdir(globalpath + 'formopac/' + filename_without_ext)                
            except:                
                None               
            mopfilepath = globalpath + 'formopac/' + filename_without_ext + '/'             
            self.mopfilepath.append(mopfilepath)            
            try:                
                shutil.move(filename, mopfilepath + inputfilename)                
            except:                
                None                
                                ####################################################################################################
            self.mopfilename.append(filename_without_ext+'.mop')
            
    def opt4dragon(self):
        for i in range(0, len(self.filename)):
            dragonpath = globalpath+'fordragon/'+self.filename_without_ext[i]+'/'+self.filename_without_ext[i]+'.mol'
            cmd = self.commandpath+"'"+self.mopfilepath[i]+self.filename[i]+"'"
            print cmd
            subprocess.Popen(cmd,shell=True).wait()
            #get the optimized orientation in out file and replace counterpart in mol file with it
            #now orientation_info is filed with optimized orientationn
                                ###############################################################################################
            cmd = 'obabel -imoo '+'\"'+self.mopfilepath[i]+self.filename_without_ext[i]+'.out\" '+'-omol -O \"'+dragonpath+'\" --gen3D'
            print cmd
            subprocess.Popen(cmd,shell=True).wait()
                                ###############################################################################################
       
    def Gasphase_MopToOut(self):
        self.GasMopfile=self.filename_without_ext+'Gas.Mop'
        f=open(self.mopfilepath+self.Mopfilename,'r')
        lines=f.readlines()
        f.close()
        lines[0]='PM6 COSMO  CHARGE=0 EF ESP GNORM=0.100 MULLIK POLAR SHIFT=80\n'
        f=open(self.mopfilepath+self.GasMopfile,'w')
        f.writelines(lines)
        f.close()
        
        if(os.path.isfile(self.mopfilepath+self.filename_without_ext+'Gas.out')==True):
            f=open(self.mopfilepath+self.filename_without_ext+'Gas.out','r')
            lines=f.readlines();
            length=len(lines)
            f.close()
            regex=".*MOPAC DONE.*"
            if(re.match(regex,lines[length-1])!=None):
                self.ParameterExtractFromOut(self.mopfilepath+self.filename_without_ext+'Gas.out')
            else:
                while(re.match(regex,lines[length-1])==None):
                    time.sleep(0.1)
                    lines=f.readlines()
                    length=len(lines)
                self.ParameterExtractFromOut(self.mopfilepath+self.filename_without_ext+'Gas.out')               
        else:
            Cmd=self.commandpath+self.mopfilepath+self.GasMopfile
            subprocess.Popen(Cmd,shell=True)
               
            #whether Gas.out does exist and out file has been produced completely
            while (os.path.isfile(self.mopfilepath+self.filename_without_ext+'Gas.out')==False) :
                continue
            #time.sleep(0.5)
            
            #to measure the out file
            #####################################################################
            f=open(self.mopfilepath+self.filename_without_ext+'Gas.out','r')
            lines=f.readlines();
            length=len(lines)
            regex=".*MOPAC DONE.*"
            while(length==0):
                lines=f.readlines();
                length=len(lines)
            while(re.match(regex,lines[length-1])==None):
                time.sleep(0.1)
                lines=f.readlines()
                length=len(lines)
            f.close()
            ###################################################################
            self.ParameterExtractFromOut(self.mopfilepath+self.filename_without_ext+'Gas.out')
    def Fluentphase_MopToOut(self):
        self.FluentMopfile=self.filename_without_ext+'Flu.Mop'
        f=open(self.mopfilepath+self.Mopfilename,'r')
        lines=f.readlines()
        f.close()
        lines[0]='PM6 eps=78.6 CHARGE=0 EF ESP GNORM=0.100 MULLIK POLAR SHIFT=80\n'
        f=open(self.mopfilepath+self.FluentMopfile,'w')
        f.writelines(lines)
        f.close()
        
        Cmd=self.commandpath+self.mopfilepath+self.FluentMopfile
        subprocess.Popen(Cmd,shell=True).wait()
        
        #self.ParameterExtractFromOut(self.mopfilepath+self.filename_without_ext+'Flu.out')
    def ParameterExtractFromOut(self,OutFile):
        self.NetAtomicCharges=[]
        self.ParameterList=[]
        j=1
        k=0
        f=open(OutFile,'r')
        lines=f.readlines()        
        f.close()
        for lineNum in range(len(lines)):
            if(re.match('.*ATOM NO\..*TYPE.*CHARGE.*No\.',lines[lineNum])!=None):
                while(re.match('.*DIPOLE.*',lines[lineNum+j])==None):
                    List=list(lines[lineNum+j].split(' '))
                    while(1):
                        try:
                            List.remove('')
                        except:
                            break
                    j=j+1
                    self.NetAtomicCharges.append(List)
                DIPOLE=lines[lineNum+j+3].split(' ')[-1]
            if(re.match('.*HEAT OF FORMATION.*',lines[lineNum])!=None):
                while(re.match('.*MOLECULAR.*DIMENSIONS.*',lines[lineNum+k])==None):

                    List=list(lines[lineNum+k].split())

                    self.ParameterList.append(List)
                    k = k+1
                    #######remove '\n' in  ParameterList
        while(1):
            try:
                self.ParameterList.remove(['\n'])
            except:
                break
        #print self.ParameterList
        try:
            HOFKCAL= float(self.ParameterList[0][5])
            HOFKJ=float(self.ParameterList[0][8])
            #print self.ParameterList[1][3]
            TE=float(self.ParameterList[1][3])
            EE=float(self.ParameterList[2][3])
            CCR=float(self.ParameterList[3][3])
            CA=float(self.ParameterList[4][3])
            CV=float(self.ParameterList[5][3])
            IonizationPotential=float(self.ParameterList[7][3])
            HOMO=float(self.ParameterList[8][5])
            LOMO=float(self.ParameterList[8][6])
            MV=float(self.ParameterList[10][3])
        except:
            print "self.ParameterList"+str(self.ParameterList)
                    ###############################################################
                    
        Qmax=-1.0
        Qmin=1.0
        for i in range(len(self.NetAtomicCharges)):
            if (float(self.NetAtomicCharges[i][2])>Qmax):
                Qmax=float(self.NetAtomicCharges[i][2])
            if (float(self.NetAtomicCharges[i][2])<Qmin):
                Qmin=float(self.NetAtomicCharges[i][2])
        QHmax=-1.0
        QHmin=1.0
        QCmax=-1.0
        QCmin=1.0
        for i in range(len(self.NetAtomicCharges)):
            if(self.NetAtomicCharges[i][1]=='H'):
                if (float(self.NetAtomicCharges[i][2])>QHmax):
                    QHmax=float(self.NetAtomicCharges[i][2])
                if (float(self.NetAtomicCharges[i][2])<QHmin):
                    QHmin=float(self.NetAtomicCharges[i][2])
            if(self.NetAtomicCharges[i][1]=='C'):
                if (float(self.NetAtomicCharges[i][2])>QCmax):
                    QCmax=float(self.NetAtomicCharges[i][2])
                if (float(self.NetAtomicCharges[i][2])<QCmin):
                    QCmin=float(self.NetAtomicCharges[i][2])
                    ##################################################################
        #polarizability
        polarizability=0.0
        length=len(lines)-1
        while(length>=0):
            if(re.match('.*ISOTROPIC.*AVERAGE.*ALPHA.*',lines[length])!=None):
                lines[length].strip()
                List=list(lines[length].split(' '))
                while(1):
                    try:
                        List.remove('')
                    except:
                        break
                polarizability=float(List[4])
                
                break
            length=length-1
        print "mop parameter computation finished"
'''
m=Mopac('ben.mop')
m.Gasphase_MopToOut()
'''
#m.ParameterExtractFromOut("/home/est863/workspace/863program/src/formopac/ben/benGas.out")
