#! /usr/bin/env python
#coding=utf-8
import datetime
from xml.dom.minidom import Document
class write_xml():
    def __init__(self):
        self.doc=Document()

    def set_tag(self,inputFilePath,OutputPath):
        
        self.tagDragon = self.doc.createElement("DRAGON")
        self.doc.appendChild(self.tagDragon)
        self.tagDragon.setAttribute("generation_date",str(datetime.datetime.now()))
        self.tagDragon.setAttribute("script_version","1")
        self.tagDragon.setAttribute("version","6.0.22")

#############OPTIONS的参数  
        self.OPTIONS = self.doc.createElement("OPTIONS")

        self.Decimal_Separator=self.doc.createElement("Decimal_Separator")
        self.Decimal_Separator.setAttribute("value",".")
        self.OPTIONS.appendChild(self.Decimal_Separator)
        
        self.Missing_String=self.doc.createElement("Missing_String")
        self.Missing_String.setAttribute("value","NaN")
        self.OPTIONS.appendChild(self.Missing_String)
        
        self.Add2DHydrogens=self.doc.createElement("Add2DHydrogens ")
        self.Add2DHydrogens.setAttribute("value","false")
        self.OPTIONS.appendChild(self.Add2DHydrogens )
        
        self.LogPathWalk=self.doc.createElement("LogPathWalk ")
        self.LogPathWalk.setAttribute("value","true")
        self.OPTIONS.appendChild(self.LogPathWalk )
        
        self.LogEdge=self.doc.createElement("LogEdge ")
        self.LogEdge.setAttribute("value","true")
        self.OPTIONS.appendChild(self.LogEdge  )

        self.Weights  = self.doc.createElement("Weights")
        self.weight=self.doc.createElement("weight")
        self.weight.setAttribute("name","Mass")
        self.Weights.appendChild(self.weight)
        self.weight=self.doc.createElement("weight")
        self.weight.setAttribute("name","VdWVolume")
        self.Weights.appendChild(self.weight )
        self.weight=self.doc.createElement("weight")
        self.weight.setAttribute("name","Electronegativity")
        self.Weights.appendChild(self.weight )
        self.weight=self.doc.createElement("weight")
        self.weight.setAttribute("name","Polarizability")
        self.Weights.appendChild(self.weight )
        self.weight=self.doc.createElement("weight")
        self.weight.setAttribute("name","Ionization")
        self.Weights.appendChild(self.weight )
        self.weight=self.doc.createElement("weight")
        self.weight.setAttribute("name","I-State")
        self.Weights.appendChild(self.weight )
        self.Weights.appendChild(self.weight)
        self.OPTIONS.appendChild(self.Weights )

        self.LogPathWalk=self.doc.createElement("LogPathWalk ")
        self.LogPathWalk.setAttribute("value","true")
        self.OPTIONS.appendChild(self.LogPathWalk )
        
        self.SaveOnlyData=self.doc.createElement("SaveOnlyData  ")
        self.SaveOnlyData.setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveOnlyData  )

        self.SaveLabelsOnSeparateFile= self.doc.createElement("SaveLabelsOnSeparateFile  ")
        self.SaveLabelsOnSeparateFile.setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveLabelsOnSeparateFile  )

        self.SaveFormatBlock= self.doc.createElement("SaveFormatBlock  ")
        self.SaveFormatBlock.setAttribute("value","%b - %n.txt")
        self.OPTIONS.appendChild(self.SaveFormatBlock  )

        self.SaveFormatSubBlock= self.doc.createElement("SaveFormatSubBlock  ")
        self.SaveFormatSubBlock.setAttribute("value","%b-%s - %n - %m.txt")
        self.OPTIONS.appendChild(self.SaveFormatSubBlock  )
        
        self.SaveExcludeMisVal = self.doc.createElement("SaveExcludeMisVal   ")
        self.SaveExcludeMisVal .setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeMisVal   )
        
        self.SaveExcludeAllMisVal= self.doc.createElement("SaveExcludeAllMisVal   ")
        self.SaveExcludeAllMisVal.setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeAllMisVal   )
        
        self.SaveExcludeConst = self.doc.createElement("SaveExcludeConst   ")
        self.SaveExcludeConst.setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeConst   )
        
        
        self.SaveExcludeNearConst= self.doc.createElement("SaveExcludeNearConst    ")
        self.SaveExcludeNearConst.setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeNearConst    )

        self.SaveExcludeStdDev = self.doc.createElement("SaveExcludeStdDev    ")
        self.SaveExcludeStdDev.setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeStdDev    )

        self.SaveStdDevThreshold = self.doc.createElement("SaveStdDevThreshold    ")
        self.SaveStdDevThreshold.setAttribute("value","0.0001")
        self.OPTIONS.appendChild(self.SaveStdDevThreshold)

        self.SaveExcludeCorrelated = self.doc.createElement("SaveExcludeCorrelated ")
        self.SaveExcludeCorrelated.setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeCorrelated )

        self.SaveCorrThreshold = self.doc.createElement("SaveCorrThreshold ")
        self.SaveCorrThreshold.setAttribute("value","0.98")
        self.OPTIONS.appendChild(self.SaveExcludeConst   )

        self.SaveExclusionOptionsToVariables = self.doc.createElement("SaveExclusionOptionsToVariables ")
        self.SaveExclusionOptionsToVariables .setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExclusionOptionsToVariables )

        #怎样设定？
        self.SaveExcludeMisMolecules = self.doc.createElement("SaveExcludeMisMolecules ")
        self.SaveExcludeMisMolecules .setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeMisMolecules)

        self.SaveExcludeRejectedMolecules  = self.doc.createElement("SaveExcludeRejectedMolecules ")
        self.SaveExcludeRejectedMolecules .setAttribute("value","false")
        self.OPTIONS.appendChild(self.SaveExcludeRejectedMolecules )
        
        #self.OPTIONS.appendChild(self.hello)
        self.tagDragon.appendChild(self.OPTIONS)
##################### 

######################descriptors的参数   参数设定完毕~~   
        self.DESCRIPTORS = self.doc.createElement("DESCRIPTORS")      
        for numbers in range(1,30):
            self.block = self.doc.createElement("block")
            self.block.setAttribute("id",str(numbers))
            self.block.setAttribute("SelectAll","true")
            self.DESCRIPTORS.appendChild(self.block)
        self.tagDragon.appendChild(self.DESCRIPTORS)
######################MOLIFILES的参数     参数设定完毕~~   
        self.MOLFILES = self.doc.createElement("MOLFILES")        
        self.molInput= self.doc.createElement("molInput")
        self.molInput.setAttribute("value","file")
        self.MOLFILES.appendChild(self.molInput  )
        
        self.molFile= self.doc.createElement("molFile ")
        self.molFile.setAttribute("value",inputFilePath)
        self.MOLFILES.appendChild(self.molFile  )
        self.tagDragon.appendChild(self.MOLFILES)
####################################   
#######################################################OUTPUT的参数  
        self.OUTPUT = self.doc.createElement("OUTPUT")
        
        self.SaveStdOut = self.doc.createElement("SaveStdOut")
        self.SaveStdOut .setAttribute("value","false")
        self.OUTPUT.appendChild(self.SaveStdOut)

        self.SaveProject= self.doc.createElement("SaveProject")
        self.SaveProject.setAttribute("value","false")
        self.OUTPUT.appendChild(self.SaveProject  )

        self.SaveProjectFile = self.doc.createElement("SaveProjectFile")
        self.SaveProjectFile.setAttribute("value","[file]")
        self.OUTPUT.appendChild(self.SaveProjectFile )

        self.SaveFile = self.doc.createElement("SaveFile ")
        self.SaveFile .setAttribute("value","true")
        self.OUTPUT.appendChild(self.SaveFile)

        self.SaveType = self.doc.createElement("SaveType  ")
        self.SaveType .setAttribute("value","singlefile")
        self.OUTPUT.appendChild(self.SaveType   )
        
        #生成结果的保存路径
        self.SaveFilePath = self.doc.createElement("SaveFilePath")
        self.SaveFilePath .setAttribute("value",OutputPath)
        self.OUTPUT.appendChild(self.SaveFilePath  )
        
        self.logMode= self.doc.createElement("logMode ")
        self.logMode.setAttribute("value","none")
        self.OUTPUT.appendChild(self.logMode )

        self.logFile= self.doc.createElement("logFile ")
        self.logFile .setAttribute("value","[file]")
        self.OUTPUT.appendChild(self.logFile )    
        self.tagDragon.appendChild(self.OUTPUT)
###################################################################  

################################################EXTERNAL参数
        #self.EXTERNAL = self.doc.createElement("EXTERNAL")
        #self.fileName = self.doc.createElement("fileName  ")
        #self.fileName.setAttribute("value","[VALUE]")
        #self.EXTERNAL.appendChild(self.fileName  )

        #self.delimiter= self.doc.createElement("delimiter ")
        
        #self.delimiter.setAttribute("value","[VALUE]")
        #self.EXTERNAL.appendChild(self.delimiter )

        #self.consecutiveDelimiter = self.doc.createElement("consecutiveDelimiter ")
        #self.consecutiveDelimiter .setAttribute("value","true")
        #self.EXTERNAL.appendChild(self.consecutiveDelimiter )

        #self.MissingValue = self.doc.createElement("MissingValue ")
        #self.MissingValue .setAttribute("value","[VALUE]")
        #self.EXTERNAL.appendChild(self.MissingValue )             
        #self.tagDragon.appendChild(self.EXTERNAL)    
        f=open(OutputPath, "w")   
        self.doc.writexml(f, "\t", "\t", "\n", "utf-8")
    def display(self):
        print self.doc.toprettyxml(indent="     ")





