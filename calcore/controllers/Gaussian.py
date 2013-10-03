#! /usr/bin/env python
#coding=utf-8
'''
Created on 2012-7-12

@author: sytmac
'''
from calcore.config.settings import  globalpath
import subprocess
from calcore.controllers.PathInit import ParseInitPath
import shutil
import re
import time
import os
import traceback
#调用不同的分子计算符软件进行分子描述符计算参数分别为DRAGON,GAUSSIAN,MOPAC

class Gaussian():
    InputExceptionFlag = False
    __ElectronstaticPotentialMeanValue = 0
    __PositiveElectronstaticPotentialMeanValue = 0
    __NegativeElectronstaticPotentialMeanValue = 0
    __MostPositiveElectronstaticPotential = 0
    __MostNegativeElectronstaticPotential = 0
    __outputNegativeNumbers = 0
    __outputPositiveNumbers = 0
    __averageDispersion = 0
    __varianceOfNegativeElectronstaticPotential = 0
    __varianceOfPositiveElectronstaticPotential = 0
    __BalanceConstant = 0
    
    __AtomicCharges = []
    __Qmin = 0.0
    __Qmax = 0.0
    
    __BindEnergy = 0.0
    __IonizationPotential = 0.0
    __ElectronAffinity = 0.0
    __ElectronProtonation = 0.0
     
    __LUMO = 0
    __HOMO = 0
    __AbsoluteHardness = 0
    __ChemicalPotential = 0
    __ElectrophilicityIndex = 0
    __CCR = 0
    togo = 0;
    def __init__(self, filePath):
        self.parse = ParseInitPath(globalpath + 'config/InitPath.xml')
        #dragon的filepath是xmlCreate生成的xml路径，默认在此文件夹中
        self.OrderPath = self.parse.get_xml_data(globalpath + 'config/InitPath.xml', 'GAUSSIAN')

        self.Inputfilename = filePath
        #to gain input file name without extension such as i.gif
        self.InputfilenameWithoutExt = self.Inputfilename.split('.')[0]
        try:   
            os.mkdir(globalpath + 'forguassian/' + self.InputfilenameWithoutExt)
        except:
            None
        self.InputFilepath = globalpath + 'forguassian/' + self.InputfilenameWithoutExt + '/'   
        try:
                shutil.move(filePath, self.InputFilepath + self.Inputfilename)
        except:
                print 'no file of .gjf to move'     
        #to amend parameter of the input file such as %chk % nproc % mem
        #################################################################################### 
        regex = "%[c,C]hk=.*"
        regex1 = "%nproc.*=[1-9]"
        regex2 = "%mem=\d{0,3}[g,G][b,B]"        
        f = open(self.InputFilepath + self.Inputfilename, 'r')
        num = 0
        lines = f.readlines()      
        f.close()
        lineNum = 0
        for line in lines:
            if re.match(regex, line) != None:
                num = num + 1
                lines[lineNum] = re.sub(regex, "%chk=" + self.InputfilenameWithoutExt + ".chk", line)       
            if re.match(regex1, line) != None:
                num = num + 1
                lines[lineNum] = re.sub(regex1, '%nproc=2', line) 
            if re.match(regex2, line) != None:
                num = num + 1
                lines[lineNum] = re.sub(regex2, '%mem=2GB', line) 
            if num == 3:
                break;
            lineNum = lineNum + 1
        f = open(self.InputFilepath + self.Inputfilename, 'w')
        f.writelines(lines)
        f.close()
        #####################################################################################
    #得到各个分子计算符软件的路径,进行命令行操作               
    def GjfParameterChange(self, Filename, regex, CommandGasPhase):
        #regex="#p.*"
        #CommandGasPhase='#p rb3lyp/6-31+g(d,p) opt freq polar'
        f = open(Filename, 'r')
        lines = f.readlines()
        lineNum = 0
        for line in lines: 
            if re.match(regex, line) != None:
                lines[lineNum] = re.sub(regex, CommandGasPhase, line) 
                break
            lineNum = lineNum + 1
        lines.append('\n\r')
        lines.append('\n\r')
        f.close()
        f = open(Filename, 'w')
        f.writelines(lines)
        f.close()
    def GjfParameterChangeAndSaveChanged(self , s_filename , l_regex , l_command_gasphase , s_savedfile=None):
        '''/
        to change the parameter of gjf file and save file as another gjf file
        s_filename:
        l_regex:  list for parameter that needs match
        l_command_gasphase : list for substitute of the parameter that we have matched 
        s_svedfile : 
        '''
        if (len(l_regex) != len(l_command_gasphase)):
            print "parameter error"
            return 
        p_fp = open(s_filename , 'r')
        l_lines = p_fp.readlines()
        i_linenum = 0
        s_replacenum = 0
        s_num = len(l_regex)
        for line in l_lines:
            for i in range(0 , len(l_regex)):
                if re.match(l_regex[i] , line) != None:
                    l_lines[i_linenum] = re.sub(l_regex[i], l_command_gasphase[i], line)
                    l_regex.pop(i)
                    l_command_gasphase.pop(i)
                    s_replacenum = s_replacenum + 1
                    break
            if s_replacenum == s_num:
                break
            i_linenum = i_linenum + 1
        p_fp.close()
        #write into save file
        if s_savedfile == None:
            pass
        else:
            p_fp = open(s_savedfile, 'w')
            l_lines.append("\n\r")
            l_lines.append("\n\r")
            p_fp.writelines(l_lines)
            p_fp.close()


    def InputFileValidityCheck(self , filelines , length , regex):
        '''/
        '''
        #print filelines     
        if(re.match(regex, filelines[length - 3]) != None):
            print "error termination"
            return False
    def GasPhaseParameterCompute(self):
        '''/
        '''
        path = self.InputFilepath + self.InputfilenameWithoutExt + '.log'
        if(os.path.exists(path) == False):
            self.GjfParameterChange(self.InputFilepath + self.Inputfilename, '#p.*', '#p rb3lyp/6-31+g(d,p) opt freq polar')       
                                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
            Cmd = self.OrderPath + self.InputFilepath + self.Inputfilename 
            subprocess.Popen(Cmd, shell=True).wait()

        #search for Mulliken atomic charges:
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.log', 'r')
        lines = f.readlines()
        length = len(lines)
        f.close()
        while(length):
            length = length - 1
            #to eject ' ' appeared in first and last position
            lines[length] = str(lines[length]).strip()
            #to find and save element and atomic charges to list
            if(re.match('Mulliken atomic charges:', lines[length]) != None):
                j = 2
                line = lines[length + j].split(' ')
                while(re.match('Sum.*', line[0]) == None):
                    List = list(line)

                    while(1):
                        try:
                            List.remove('')
                        except:
                            break
                    List.pop(0)
                    j = j + 1
                    line = lines[length + j].split(' ')
                    self.__AtomicCharges.append(List)
                break
        print "GasPhaseParameterCompute has been finished"
    def Gasoptlogfile_produce(self):
        self.GjfParameterChange(self.InputFilepath + self.Inputfilename, '#p.*', '#p rb3lyp/6-31+g(d,p) opt freq polar')       
                            #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd = self.OrderPath + self.InputFilepath + self.Inputfilename + ' ' + self.InputfilenameWithoutExt + '.log'
        subprocess.Popen(Cmd, shell=True).wait()          
        print "Gasoptlogfile_produce has been finished " 
    def IPlogfile_produce(self):
        #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd = self.OrderPath + self.InputFilepath + self.Inputfilename + ' ' + self.InputfilenameWithoutExt + '.IPlog'
        subprocess.Popen(Cmd, shell=True).wait()
        print "IPlogfile_produce has been finished "
    def EAlogfile_produce(self):
                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd = self.OrderPath + self.InputFilepath + self.Inputfilename + ' ' + self.InputfilenameWithoutExt + '.EAlog'
        subprocess.Popen(Cmd, shell=True).wait()

        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.EAlog', 'r')
        lines = f.readlines();
        length = len(lines)
        regex = ".*Normal termination.*"
        while(length == 0):
            lines = f.readlines();
            length = len(lines)
        #print "length of Gasoptlog:"+str(length)
        while(re.match(regex, lines[length - 1]) == None):
            time.sleep(1)                  
            if(length == 0):
                continue
            else:
                f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.EAlog', 'r')
                lines = f.readlines()            
                length = len(lines)
                f.close()
                print str(length) + ' ' + lines[length - 1]
                #break
        f.close()
                    ###################################################################
        print "EAlogfile_produce has been finished "
    def EPlogfile_produce(self):
                        #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        Cmd = self.OrderPath + self.InputFilepath + self.Inputfilename + ' ' + self.InputfilenameWithoutExt + '.EPlog'
        subprocess.Popen(Cmd, shell=True).wait()

                    ###################################################################
    def GasPhase_MolecularDipoleMoment(self):
        #first search for'completed'appeared first time 
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.log', 'r')       
        lines = f.readlines()
        f.close()
        for i in range(len(lines)):
            if(re.match('.*completed.*', lines[i]) != None):
                j = i + 1
                while(j < len(lines)):
                    if(re.match('.*Tot=.*', lines[j]) != None):
                        DipoleMomentline = re.findall('Tot=.*', lines[j])
                        DipoleMoment = float(str(DipoleMomentline[0]).split(' ')[-1])
                        print DipoleMoment
                        break
                    j = j + 1
                break
        
        return DipoleMoment
    def GasPhase_MolecularPolarizability(self):
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.log', 'r')
        lines = f.readlines()
        f.close()
        for i in range(len(lines)):
            if(re.match('.*Isotropic polarizability.*', lines[i]) != None):
                Polarizability = float(str(lines[i]).split(' ')[-2])
                print Polarizability
                print '\n'
                break
        del lines
        return Polarizability
    def GasPhase_MolecularVolume(self):
        #to create gjf file for computing

        # save standard orientation in log file
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.log', 'r')
        lines = f.readlines()
        f.close()
        lineNum = len(lines) - 1
        while((lineNum >= 0)and(re.match('.*Standard orientation:.*', lines[lineNum]) == None)):
            lineNum = lineNum - 1
        lineNum = lineNum + 5
        orientationLines = []
        #lines of standard orientation
        orientationLineNum = 0
        while(re.match('.*----.*', lines[lineNum]) == None):
            orientationLines.append(lines[lineNum].split()[-3] + ' ' + lines[lineNum].split()[-2] + ' ' + lines[lineNum].split()[-1])
            orientationLineNum = orientationLineNum + 1
            lineNum = lineNum + 1
        #to revise .gjf file with standard orientation 
        #to reviese .ipgjf
        l_regex = ["#p.*" , ]
        l_command_gasphase = ['#p sp volume' ,]
        self.GjfParameterChangeAndSaveChanged(self.InputFilepath + self.Inputfilename , l_regex , l_command_gasphase , self.InputFilepath+self.InputfilenameWithoutExt + '.MVgjf')
        ############################################################################################################
        Cmd = self.OrderPath + self.InputFilepath + self.Inputfilename +' '+self.InputfilenameWithoutExt+'.MVlog'
        subprocess.Popen(Cmd, shell=True).wait()
        #search the prduced .log file for Molar volme

        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.MVlog', 'r')
        Loglines = f.readlines()
        f.close()        
        regex = ".*Molar volume =.*"
        for Logline in Loglines:      
            if (re.match(regex, Logline) != None):
                volume = Logline.split(' ')[-2]
                print 'volume: ' + volume
                break
    def GasPhase_MolecularHOMOAndLUMOAndAbsolut_Hardness(self):
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.log', 'r')
        lines = f.readlines()
        f.close()
        regex = '.*Alpha  occ. eigenvalues.*'
        for lineNum in range(len(lines)):
            if(re.match(regex, lines[lineNum]) != None):
                while(re.match(regex, lines[lineNum]) != None):
                    lineNum = lineNum + 1
                List = list(lines[lineNum].split(' '))
                while(1):
                    try:
                        List.remove('')
                    except:
                        break
                self.__LUMO = List[4]
                self.__HOMO = lines[lineNum - 1].split(' ')[-1]
                break
        self.__AbsoluteHardness = (float(self.__HOMO) - float(self.__LUMO)) / 2
        #print 'AbsoluteHardness: '+str(self.__AbsoluteHardness)
        self.__ChemicalPotential = (float(self.__HOMO) + float(self.__LUMO)) / 2
        try:
            self.__ElectrophilicityIndex = pow(float(self.__ChemicalPotential), 2) / (2 * self.__AbsoluteHardness)
        except:
            print "divisor self.__AbsoluteHardness:" + str(self.__AbsoluteHardness)
        #print self.__ElectrophilicityIndex
        del lines

    def GasPhase_CCR(self):      
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.log', 'r')
        lines = f.readlines()
        f.close()
        regex = '.*N-N=.*'
        lineNum = len(lines) - 1
        while(lineNum >= 0):
            if(re.match(regex, lines[lineNum]) != None):
                List = list(lines[lineNum].split(' '))
                while(1):
                    try:
                        List.remove('')
                    except:
                        break
                self.__CCR = List[1]
                #print self.__CCR
                break
            lineNum = lineNum - 1
    def GasBindEnergy(self):
        path = self.InputFilepath + self.InputfilenameWithoutExt + '.log'
        if(os.path.exists(path) == False):
            self.Gasoptlogfile_produce()    
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.log', 'r')
        lines = f.readlines() 
        f.close()  
        length = len(lines) - 1
        while(length >= 0):
            if(re.match('.*SCF Done.*', lines[length]) != None):
                List = list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__BindEnergy = float(List[4])            
                break
            length = length - 1

    def GasPhase_IonizationPotential(self):
        '''/
        first : use key words "#p opt freq" to optimize the molecular
        second: to search "standard orientation" in log file
        third : use key words "#p sp"and change charge number
        '''
        l_regex = ["#p.*"  ]
        l_command_gasphase = ['#p opt freq' , ]
        self.GjfParameterChangeAndSaveChanged(self.InputFilepath + self.Inputfilename , l_regex , l_command_gasphase , self.InputFilepath + self.InputfilenameWithoutExt + '.IPgjf')
                    #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        if os.path.isfile(self.InputFilepath + self.InputfilenameWithoutExt + '.freqOptlog'):
            pass
        else:
            Cmd = self.OrderPath + self.InputFilepath + self.InputfilenameWithoutExt + '.IPgjf' + ' ' + self.InputfilenameWithoutExt + '.freqOptlog'
            subprocess.Popen(Cmd, shell=True).wait()             

                    ###################################################################
        # save standard orientation in log file
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.freqOptlog', 'r')
        lines = f.readlines()
        f.close()
        lineNum = len(lines) - 1
        while((lineNum >= 0)and(re.match('.*Standard orientation:.*', lines[lineNum]) == None)):
            lineNum = lineNum - 1
        lineNum = lineNum + 5
        orientationLines = []
        orientationLineNum = 0
        while(re.match('.*----.*', lines[lineNum]) == None):
            orientationLines.append(lines[lineNum].split()[-3] + ' ' + lines[lineNum].split()[-2] + ' ' + lines[lineNum].split()[-1])
            orientationLineNum = orientationLineNum + 1
            lineNum = lineNum + 1
            ##########################################################################################################
            #to reviese .ipgjf
        l_regex = ["#p.*" , "^0.?1" ]
        l_command_gasphase = ['#p sp' , '1 2']
        self.GjfParameterChangeAndSaveChanged(self.InputFilepath + self.Inputfilename , l_regex , l_command_gasphase ,)
            ##########################################################################################################
            #to revise .ipgjf file with standard orientation 
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.IPgjf', 'r')
        GjfLines = f.readlines()
        f.close()
        lineNum = len(GjfLines) - 1
        while(cmp(GjfLines[lineNum], '\r\n') == 0):
            lineNum = lineNum - 1
        oritationLineNum = 0
        for i in range(lineNum - orientationLineNum + 1, lineNum + 1):
            try:   
                s = ' ' + GjfLines[i].split(' ')[1] + '     ' + orientationLines[oritationLineNum].split(' ')[0] + '    ' + orientationLines[oritationLineNum].split(' ')[1] + '    ' + orientationLines[oritationLineNum].split(' ')[2] + '\r\n'
                oritationLineNum = oritationLineNum + 1
                GjfLines[i] = s
            except:
                pass
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.IPgjf', 'w')
        f.writelines(GjfLines)
        f.close()
        del GjfLines
        ###################################################################################################
        #to produce .IPlog file 
        path = self.InputFilepath + self.InputfilenameWithoutExt + '.IPlog'
        if(os.path.exists(path) == False):
            self.IPlogfile_produce()
        #######################################################################################################3
        #to search scf done in IPlog file
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.IPlog', 'r')
        lines = f.readlines() 
        f.close()  
        length = len(lines) - 1
        while(length >= 0):
            if(re.match('.*SCF Done.*', lines[length]) != None):
                List = list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__IonizationPotential = float(List[4])           
                break
            length = length - 1    
        print  self.__IonizationPotential
    
    def GasPhase_ElectronAffinity(self):
        '''/
        first : use key words "#p opt freq" to optimize the molecular
        second: to search "standard orientation" in log file
        third : use key words "#p sp"and change charge number
        '''
        l_regex = ["#p.*"  ]
        l_command_gasphase = ['#p opt freq' , ]
        self.GjfParameterChangeAndSaveChanged(self.InputFilepath + self.Inputfilename , l_regex , l_command_gasphase , self.InputFilepath + self.InputfilenameWithoutExt + '.EAgjf')
                    #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        if os.path.isfile(self.InputFilepath + self.InputfilenameWithoutExt + '.freqOptlog'):
            pass
        else:
            Cmd = self.OrderPath + self.InputFilepath + self.InputfilenameWithoutExt + '.EAgjf' + ' ' + self.InputfilenameWithoutExt + '.freqOptlog'
            subprocess.Popen(Cmd, shell=True)              
        while(1):
            try:
                f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.freqOptlog', 'r')
                break
            except:
                continue
        #####################################################################to check the file to the end
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.freqOptlog', 'r')
        lines = f.readlines();
        length = len(lines)
        regex = ".*Normal termination.*"
        regex2 = ".*Error termination.*"
        while(length == 0):
            lines = f.readlines();
            length = len(lines)
        while(re.match(regex, lines[length - 1]) == None):
            time.sleep(1)                  
            if(length == 0):
                continue
            else:
                f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.freqOptlog', 'r')
                lines = f.readlines()            
                length = len(lines)
                f.close()
                if(self.InputFileValidityCheck(lines, length, regex2) == False):
                    self.InputExceptionFlag = True
                    return;                
        f.close()
                    ###################################################################
        # save standard orientation in log file
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.freqOptlog', 'r')
        lines = f.readlines()
        f.close()
        lineNum = len(lines) - 1
        while((lineNum >= 0)and(re.match('.*Standard orientation:.*', lines[lineNum]) == None)):
            lineNum = lineNum - 1
        lineNum = lineNum + 5
        orientationLines = []
        orientationLineNum = 0
        while(re.match('.*----.*', lines[lineNum]) == None):
            orientationLines.append(lines[lineNum].split()[-3] + ' ' + lines[lineNum].split()[-2] + ' ' + lines[lineNum].split()[-1])
            orientationLineNum = orientationLineNum + 1
            lineNum = lineNum + 1
            ##########################################################################################################
            #to reviese .ipgjf
        l_regex = ["#p.*" , "^0.?1" ]
        l_command_gasphase = ['#p sp' , '1 2']
        self.GjfParameterChangeAndSaveChanged(self.InputFilepath + self.Inputfilename , l_regex , l_command_gasphase ,)
            ##########################################################################################################
            #to revise .ipgjf file with standard orientation 
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.EAgjf', 'r')
        GjfLines = f.readlines()
        f.close()
        lineNum = len(GjfLines) - 1
        while(cmp(GjfLines[lineNum], '\r\n') == 0):
            lineNum = lineNum - 1
        oritationLineNum = 0
        for i in range(lineNum - orientationLineNum + 1, lineNum + 1):
            try:   
                s = ' ' + GjfLines[i].split(' ')[1] + '     ' + orientationLines[oritationLineNum].split(' ')[0] + '    ' + orientationLines[oritationLineNum].split(' ')[1] + '    ' + orientationLines[oritationLineNum].split(' ')[2] + '\r\n'
                oritationLineNum = oritationLineNum + 1
                GjfLines[i] = s
            except:
                pass
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.EAgjf', 'w')
        f.writelines(GjfLines)
        f.close()
        del GjfLines
        ###################################################################################################
        #to produce .IPlog file 
                    #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        if os.path.isfile(self.InputFilepath + self.InputfilenameWithoutExt + '.EAlog'):
            pass
        else:
            Cmd = self.OrderPath + self.InputFilepath + self.InputfilenameWithoutExt + '.EAgjf' + ' ' + self.InputfilenameWithoutExt + '.EAlog'
            subprocess.Popen(Cmd, shell=True)              
        while(1):
            try:
                f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.EAlog', 'r')
                break
            except:
                continue
        #######################################################################################################3
        #to search scf done in IPlog file
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.EAlog', 'r')
        lines = f.readlines() 
        f.close()  
        length = len(lines) - 1
        while(length >= 0): 
            if(re.match('.*SCF Done.*', lines[length]) != None):
                List = list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__IonizationPotential = float(List[4])           
                break
            length = length - 1    
        print  'self.__IonizationPotential:'+str(self.__IonizationPotential)
    def GasPhase_EnergyProtonation(self):
        l_regex = ["#p.*"  ]
        l_command_gasphase = ['#p opt freq' , ]
        self.GjfParameterChangeAndSaveChanged(self.InputFilepath + self.Inputfilename , l_regex , l_command_gasphase , self.InputFilepath + self.InputfilenameWithoutExt + '.EPgjf')
        
        #use g09 to compute parameter
        #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
        if os.path.isfile(self.InputFilepath + self.InputfilenameWithoutExt + '.EPlog'):
            pass
        else:
            Cmd = self.OrderPath + self.InputFilepath + self.InputfilenameWithoutExt + '.EPgjf' + ' ' + self.InputfilenameWithoutExt + '.EPlog'
            subprocess.Popen(Cmd, shell=True).wait()             
        #parameter search
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.EPlog', 'r')
        lines = f.readlines() 
        f.close()  
        length = len(lines) - 1
        while(length >= 0):
            if(re.match('.*SCF Done.*', lines[length]) != None):
                List = list(lines[length].split(' '))
                while(1):
                        try:
                            List.remove('')
                        except:
                            break
                self.__ElectronProtonation = float(List[4])           
                break
            length = length - 1    
        print 'GasPhase_EnergyProtonation has been finished : '
    def GasPhase_QmaxAndQmin(self):

            ##########################################################################################################################
        #compute the parameter that required
        Qmin = 0.0
        Qmax = 0.0
        for i in range(len(self.__AtomicCharges)):
            if(float(self.__AtomicCharges[i][1]) > Qmax):
                Qmax = float(self.__AtomicCharges[i][1])
            elif(float(self.__AtomicCharges[i][1]) < Qmin):
                Qmin = float(self.__AtomicCharges[i][1])
        self.__Qmax = Qmax
        self.__Qmin = Qmin
            ##########################################################################################################################
    def GasPhase_QAB(self, A, B):
        sum = 0
        for i in range(len(self.__AtomicCharges)):
            if((cmp(self.__AtomicCharges[i][0], A) == 0)or(cmp(self.__AtomicCharges[i][0], B) == 0)):
                sum = sum + float(self.__AtomicCharges[i][1])
        return sum
    def GasPhase_QTSquare(self):
        squareSum = 0
        for i in range(len(self.__AtomicCharges)):
            squareSum = squareSum + pow(float(self.__AtomicCharges[i][1]), 2)
        #print 'GasPhase_QTSquare: '+str(squareSum)
        return squareSum
    def GasPhase_QASquare(self, A):
        squareSum = 0
        for i in range(len(self.__AtomicCharges)):
            if(cmp(self.__AtomicCharges[i][0], A) == 0):
                squareSum = squareSum + pow(float(self.__AtomicCharges[i][1]), 2)
        #print 'GasPhase_QASquare: '+str(squareSum)
        return squareSum   
    def GasPhase_AverageAbsoluteValue(self):
        SumOfAbsoluteValue = 0.0
        for i in range(len(self.__AtomicCharges)):
            SumOfAbsoluteValue = SumOfAbsoluteValue + abs(float(self.__AtomicCharges[i][1]))
        AverageAbsoluteValue = SumOfAbsoluteValue / len(self.__AtomicCharges)
        print 'GasPhase_AverageAbsoluteValue: ' + str(AverageAbsoluteValue)
        return AverageAbsoluteValue
    def GasPhase_PPCG(self):
        Qmax = self.__Qmax
        PositiveSum = 0
        for i in range(len(self.__AtomicCharges)):
            if(float(self.__AtomicCharges[i][1]) > 0):
                PositiveSum = PositiveSum + float(self.__AtomicCharges[i][1])
        PPCG = Qmax / PositiveSum
        #print 'PPCG'+str(PPCG)
        return PPCG
    def GasPhase_RNGG(self):
        Qmin = self.__Qmin
        NegativeSum = 0
        for i in range(len(self.__AtomicCharges)):
            if(float(self.__AtomicCharges[i][1]) < 0):
                NegativeSum = NegativeSum + float(self.__AtomicCharges[i][1])
        RNGG = Qmin / NegativeSum
        #print 'RNGG'+str(RNGG)
        return RNGG
    def FluentPhaseParameterCompute(self):
        path = self.InputFilepath + self.InputfilenameWithoutExt + '.Fluoptlog'
        if(os.path.exists(path) == False):
            self.GjfParameterChange(self.InputFilepath + self.Inputfilename, '#p.*', '#p rb3lyp/6-31+g(d,p) opt freq scrf=(iefpcm,solvent=water)')       
                                #进入针对xml解析的计算分子描述符原始文件的路径,进行计算
            Cmd = self.OrderPath + self.InputFilepath + self.Inputfilename + ' ' + self.InputfilenameWithoutExt + '.Fluoptlog'
            subprocess.Popen(Cmd, shell=True).wait()
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.Fluoptlog', 'r')
        lines = f.readlines();
        length = len(lines)
        regex = ".*Normal termination.*"
        while(length == 0):
            lines = f.readlines();
            length = len(lines)
        while(re.match(regex, lines[length - 1]) == None):
            time.sleep(1)                  
            if(length == 0):
                continue
            else:
                f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.Fluoptlog', 'r')
                lines = f.readlines()            
                length = len(lines)
                f.close()
                break
        f.close()
            ####################################################################################################
        #search for Mulliken atomic charges:
        f = open(self.InputFilepath + self.InputfilenameWithoutExt + '.Fluoptlog', 'r')
        lines = f.readlines()
        #print length
        length = len(lines)
        f.close()
        while(length):
            length = length - 1
            #to eject ' ' appeared in first and last position
            lines[length] = str(lines[length]).strip()
            #to find and save element and atomic charges to list
            if(re.match('Mulliken atomic charges:', lines[length]) != None):
                j = 2
                line = lines[length + j].split(' ')
                while(re.match('Sum.*', line[0]) == None):
                    List = list(line)
                    while(1):
                        try:
                            List.remove('')
                        except:
                            break
                    List.pop(0)
                    j = j + 1
                    line = lines[length + j].split(' ')
                    self.__AtomicCharges.append(List)
                    #print AtomicCharges
                    #print '\n'
                break
    #compute electronstaticpotential with gsgrid
    def Gaussian_electronstaticpotential_chkTofchk(self):
            while(1):              
                if(os.path.isfile(globalpath +'controllers/'+self.InputfilenameWithoutExt + '.chk')):
                    Cmd = 'formchk ' + globalpath +'controllers/'+ self.InputfilenameWithoutExt + '.chk'                            
                    subprocess.Popen(Cmd, shell=True).wait()
                    print "formchk has been finished"
                    # to produce fchk file completely
                    
                    break
                else:
                    print globalpath + 'controllers'+'controllers/'+self.InputfilenameWithoutExt + '.chk'
                    print"chk file doesn't exist"
                    continue
            while(1):
                try:
                    shutil.move(globalpath + 'controllers/'+self.InputfilenameWithoutExt + '.fchk', self.InputFilepath + self.InputfilenameWithoutExt + '.fchk')
                    break;
                except:
                    print 'no file of .fck to move'
    #transform fchk into cub in globalpath and other path doesn't work
    def Gaussian_electronstaticpotential_fckTocub(self):
                Cmd = 'cubegen 0 density=scf ' + self.InputFilepath + self.InputfilenameWithoutExt + '.fchk' + ' ' + globalpath + self.InputfilenameWithoutExt + '_density.cub 0 h'

                subprocess.Popen(Cmd, shell=True).wait()
                Cmd = 'cubegen 0 potential=scf ' + self.InputFilepath + self.InputfilenameWithoutExt + '.fchk' + ' ' + globalpath + self.InputfilenameWithoutExt + '_potential.cub 0 h'
                subprocess.Popen(Cmd, shell=True).wait()

         
    def Gaussian_electronstaticpotential_output(self):

        arg1 = globalpath + self.InputfilenameWithoutExt + '_density.cub'
        arg2 = ' 12'
        arg3 = ' 0.0001'
        arg4 = ' 4'
        arg5 = globalpath + self.InputfilenameWithoutExt + '_potential.cub'
        arg6 = ' n'
        p = subprocess.Popen(['/home/est863/gsgrid1.7_src/gsgrid', ], stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        
        #subprocess.Popen.communicate(self, input)
        #p.stdin.write(arg0)
        p.stdin.write('\'' + arg1 + '\'' + '\n')
        p.stdin.write(arg2 + '\n')
        p.stdin.write(arg3 + '\n')
        p.stdin.write(arg4 + '\n')
        p.stdin.write('\'' + arg5 + '\'' + '\n')
        p.stdin.write(arg6 + '\n')
        p.stdin.write('s' + '\n')
        p.wait()
    def Gaussian_electronstaticpotential_parameterCompute(self):
        print "Gaussian_electronstaticpotential_parameterCompute begins"
        #deal with output.txt  output_positive.txt output_negtive.txt 
        #first move them to InputFilepath dictionary
        while(1):
            if(os.path.isfile('output.txt')):
                shutil.move('output.txt', self.InputFilepath + 'output.txt')
                print "output.txt found"
                break;
            else:
                continue
        while(1):
            try:
                p_fp=open(self.InputFilepath + 'output.txt','r')
                break
            except:
                continue
        l_lines = p_fp.readlines()
        s_len = len(l_lines)
        l_neg_lines = []
        l_pos_lines = []
        '''use output.txt to produce positive/negative file'''
        for i in range(0 , s_len):
            if float( l_lines[i].split(' ')[-1]) < 0:
                l_neg_lines.append(l_lines[i])
            else:
                l_pos_lines.append(l_lines[i])

        p_fp.close()     
        p_fp_neg = open(self.InputFilepath + 'output_negative.txt' , 'w')
        p_fp_pos = open(self.InputFilepath + 'output_positive.txt' , 'w')  
        p_fp_neg.writelines(l_neg_lines)
        p_fp_pos.writelines(l_pos_lines)
        p_fp_neg.close()
        p_fp_pos.close()

        #to get __PositiveElectronstaticPotentialMeanValue,__MostPositiveElectronstaticPotential,__varianceOfPositiveElectronstaticPotential
        sum = 0
        MostPositiveElectronstaticPotential = 0.000001
        while(1):
            try:
                Positivelines = list(open(self.InputFilepath + 'output_positive.txt'))
                break
            except:
                time.sleep(0.1)
        for i in range(0, len(Positivelines)):
            tempFloat = float(Positivelines[i].split(' ')[-1])
            if(tempFloat > MostPositiveElectronstaticPotential):
                MostPositiveElectronstaticPotential = tempFloat
            sum = sum + float(Positivelines[i].split(' ')[-1])
        self.__PositiveElectronstaticPotentialMeanValue = sum / len(Positivelines)
        self.__MostPositiveElectronstaticPotential = MostPositiveElectronstaticPotential
        PositiveVarianceSum = 0.0
        for i in range(0, len(Positivelines)):
            tempFloat = float(Positivelines[i].split(' ')[-1])
            PositiveVarianceSum = PositiveVarianceSum + pow((tempFloat - self.__PositiveElectronstaticPotentialMeanValue), 2)
        self.__varianceOfPositiveElectronstaticPotential = PositiveVarianceSum / len(Positivelines)
        #print str(self.__varianceOfPositiveElectronstaticPotential)+'\n'
        #print'self.__MostPositiveElectronstaticPotential'+str(self.__MostPositiveElectronstaticPotential)+'\n'
        #print 'self.__PositiveElectronstaticPotentialMeanValue: '+str(self.__PositiveElectronstaticPotentialMeanValue)+'\n'
        #to gain __negativeEkectronstaticPotentianlMeanValue,__MostNegativeElectronstaticPotential,__varianceOfNegativeElectronstaticPotential
        sum = 0
        MostNegativeElectronstaticPotential = -0.000001
        while(1):
            try:
                Negativelines = list(open(self.InputFilepath + 'output_negative.txt'))
                break
            except:
                time.sleep(0.1)
        for i in range(0, len(Negativelines)):
            tempFloat = float(Negativelines[i].split(' ')[-1])
            if(tempFloat < MostNegativeElectronstaticPotential):
                MostNegativeElectronstaticPotential = tempFloat           
            sum = sum + float(Negativelines[i].split(' ')[-1])
        self.__MostNegativeElectronstaticPotential = MostNegativeElectronstaticPotential
        self.__NegativeElectronstaticPotentialMeanValue = sum / len(Negativelines)
        NegativeVarianceSum = 0
        for i in range(0, len(Negativelines)):
            tempFloat = float(Negativelines[i].split(' ')[-1])
            NegativeVarianceSum = NegativeVarianceSum + pow((tempFloat - self.__NegativeElectronstaticPotentialMeanValue), 2)
        self.__varianceOfNegativeElectronstaticPotential = NegativeVarianceSum / len(Negativelines)
        
        print str(self.__varianceOfNegativeElectronstaticPotential)+'\n'
        print 'self.__MostNegativeElectronstaticPotential'+str(self.__MostNegativeElectronstaticPotential)+'\n'
        print 'self.__NegativeElectronstaticPotentialMeanValue: '+str(self.__NegativeElectronstaticPotentialMeanValue)+'\n'
        #to get __ElectronstaticPotentialMeanValue
        sum = 0
        while(1):
            try:
                lines = list(open(self.InputFilepath + 'output.txt'))
                break
            except:
                time.sleep(0.1)
        for i in range(0, len(lines)):
            sum = sum + float(lines[i].split(' ')[-1])
        self.__ElectronstaticPotentialMeanValue = sum / len(lines)
            
        sum = 0
        #to get averageDispersion
        lines = list(open(self.InputFilepath + 'output.txt'))
        for i in range(0, len(lines)):
            tempFloat = float(lines[i].split(' ')[-1])
            if(tempFloat <= -0.000001):
                self.__outputNegativeNumbers = self.__outputNegativeNumbers + 1
            elif(tempFloat >= 0.000001):
                self.__outputPositiveNumbers = self.__outputPositiveNumbers + 1
            sum = sum + abs(tempFloat - self.__ElectronstaticPotentialMeanValue)
        self.__averageDispersion = sum / len(lines)
        print 'averageDispersion is' + str(self.__averageDispersion) + '\n'
        print '__outputNegativeNumbers:' + str(self.__outputNegativeNumbers) + '\n'
        print '__outputPositiveNumbers:' + str(self.__outputPositiveNumbers)
        #to get  balanceOncstant
        self.__BalanceConstant = (self.__varianceOfNegativeElectronstaticPotential * self.__varianceOfPositiveElectronstaticPotential) / pow((self.__varianceOfNegativeElectronstaticPotential + self.__varianceOfPositiveElectronstaticPotential), 2)
        print 'self.__BalanceConstant: ' + str(self.__BalanceConstant) + '\n'
        #remove file in src
        try:

            shutil.move(globalpath + self.InputfilenameWithoutExt + '_density.cub', self.InputFilepath + self.InputfilenameWithoutExt + '_density.cub')

            shutil.move(globalpath + self.InputfilenameWithoutExt + '_potential.cub', self.InputFilepath + self.InputfilenameWithoutExt + '_potential.cub')
        except Exception, e:
            exstr = traceback.format_exc()
            print exstr  
