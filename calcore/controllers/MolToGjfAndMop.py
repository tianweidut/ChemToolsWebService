#! /usr/bin/env python
#coding=utf-8
'''
Created on 2012-7-30

@author: sytmac
'''
def Mol2GjfandMop(file,gjf=False, mop=False):
    #to gain input file name such as i.gif
    Inputfilename=file.split('/')[-1]
    #to gain input file name without extension such as i.gif
    InputfilenameWithoutExt=Inputfilename.split('.')[0]
    OritationList=[]
    f=open(file,'r')
    lines=f.readlines()
    f.close()
    for lineNum in range(0 , len(lines)):
        try:
            List=list(lines[lineNum].split())
            if(List[3]>'A'and List[3]<'Z'):     
                OritationList.append(' '+List[3]+'             '+List[0]+'    '+List[1]+'    '+List[2]+'\n')
        except:
            continue                                        
    if gjf == True:
        GjfList=[]   
        GjfList.append('%chk='+InputfilenameWithoutExt+'.chk\n')
        GjfList.append('%nproc=2\n')
        GjfList.append('%mem=2GB\n')
        GjfList.append('#p rb3lyp/6-31+g(d,p)\n')
        GjfList.append('\n')
        GjfList.append('Title Card Required\n')
        GjfList.append('\n')
        GjfList.append('0 1\r')
        GjfList.extend(OritationList)
        GjfList.append('\n\n')
        f=open(file.split('.')[0]+'.gjf','w')
        f.writelines(tuple(GjfList))
        f.close()
    if mop == True:
        MopList=[]
        MopList.append(' PM3 CHARGE=0 GNORM=0.100  static\n')
        MopList.append('\n\r\n')
        MopList.extend(OritationList)
        f=open(file.split('.')[0]+'.mop','w')
        f.writelines(tuple(MopList))
        f.close()
#Mol2GjfandMop('/home/est863/workspace/863program/src/controllers/C(Cl)(Cl)(Cl)C.mol', mop = True)