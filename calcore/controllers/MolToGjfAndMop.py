#! /usr/bin/env python
#coding=utf-8
'''
Created on 2012-7-30

@author: sytmac
'''
def Mol2GjfandMop(file,modeltype=None,gjf=False, mop=False):
    #to gain input file name such as i.gif
    print "in the Mol2GjfandMop"
    print modeltype
    if modeltype==3:
        element=dict.fromkeys(['H','C','N','O','F','P','S','Cl','Se','Br','I','Si','Hg','Pb'],0)
    #print element
    Inputfilename=file.split('/')[-1]
    #to gain input file name without extension such as i.gif
    InputfilenameWithoutExt=Inputfilename.split('.')[0]
    OritationList=[]
    print file
    f=open(file,'r')
    lines=f.readlines()
    f.close()
    for lineNum in range(0 , len(lines)):
        try:
            List=list(lines[lineNum].split())
            if(List[3]>'A'and List[3]<'Z'):     
                OritationList.append(' '+List[3]+'             '+List[0]+'    '+List[1]+'    '+List[2]+'\n')
                if modeltype==3:
                    element[List[3]]=1
                    #print List[3]
                    #print element[List[3]]
        except:
            continue                                       
    if gjf == True:
        print "gjf=true"
        GjfList=[]   
        GjfList.append('%chk='+InputfilenameWithoutExt+'.chk\n')
        GjfList.append('%nproc=2\n')
        GjfList.append('%mem=2GB\n')
        if modeltype==3:
            if (element['I']|element['Si']|element['Hg']|element['Pb'])==1:
                GjfList.append('#p opt freq b3lyp/genecp scf=tight int=ultrafine\n')
                #print "to do B"
            else:
                GjfList.append('#p opt freq b3lyp/6-311+G(d,p) scf=tight int=ultrafine\n')
        elif modeltype==2:
            GjfList.append('#p opt freq b3lyp/6-31+g(d,p) SCRF=(IEFPCM,SOLVENT=WATER)\n')
        GjfList.append('\n')
        GjfList.append('Title Card Required\n')
        GjfList.append('\n')
        GjfList.append('0 1\n')
        GjfList.extend(OritationList)
        GjfList.append('\n')
        tempC=""
        tempHg=""
        if modeltype==3 and (element['I']|element['Si']|element['Hg']|element['Pb'])==1:
            templist=('I','Si','Hg','Pb')
            for temp in templist:
                if element[temp]==1:
                    tempHg=tempHg+temp+" "
                    element[temp]=0

            for key in element:
                if element[key]==1:
                    tempC=tempC+key+" "
            GjfList.append(tempC+'0\n')
            GjfList.append('6-31+g(d,p)\n')
            GjfList.append('****\n')
            GjfList.append(tempHg+'0\n')
            GjfList.append('LANL2DZ\n')
            GjfList.append('****\n\n')
            GjfList.append(tempHg+'0\n')
            GjfList.append('LANL2DZ\n\n')

        f=open(file.split('.')[0]+'.gjf','w')
        f.writelines(tuple(GjfList))
        f.close()
        print "Mol2GjfandMop-gjf close"
    if mop == True:
        print "mop=True"
        MopList=[]
        MopList.append('EF GNORM=0.0001 MMOK GEO-OK PM3\n')
        #MopList.append('opt freq b3lyp/6-31+g(d,p) SCRF=(IEFPCM,SOLVENT=WATER)\n')
        MopList.append('\n\r\n')
        MopList.extend(OritationList)
        f=open(file.split('.')[0]+'.mop','w')
        f.writelines(tuple(MopList))
        f.close()
        print "Mol2GjfandMop-mop close"
#Mol2GjfandMop('/home/est863/workspace/863program/src/controllers/C(Cl)(Cl)(Cl)C.mol', mop = True)
