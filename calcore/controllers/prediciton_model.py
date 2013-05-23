'''
Created on 2012-12-4

@author: SongYang
'''
from calcore.controllers.Dragon import Dragon
class PredictionModel_ForParamInDragon(object):
    '''
this class is used for model computation that parameters needed in Dragon output file
    '''
    def __init__(self , modelname=None ,para={}):
        self.predict_result = {}
        para = para or {}
        #start to compute model  results
        d = Dragon(smiles_str=para["smilestring"], molfile=para["filename"])
        d.mol2drs()
        self.predict_result["invalidnums"] = d.invalidnums
        modelname = modelname or []
        for name in modelname:
            self.models_computation(name, para ,d)
        print self.predict_result 
    def models_computation(self, modelname, para ,instance_of_dragon):
                    {
         "logKOA" :  lambda para:self.logKOA(para ,instance_of_dragon),
         "logRP"  :  lambda para:self.logRP(para ,instance_of_dragon),
         
        }[modelname](para)
    def logKOA(self, para ,d):
        '''
        logKOA model computation
        '''
        abstract_value = d.extractparameter(["X1sol", "Mor13v", "HATS5v", "RDF035m","Mor15u" ,"RDF090m", "H-050", "nRCOOR", "R5v", "T(O..Cl)", "RCI","nRCOOR"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logKOA'] = 0.509 + 0.986*float(abstract_value[smilenum]['X1sol'])-1.018*float(abstract_value[smilenum]['Mor13v'])+ \
            1.384*float(abstract_value[smilenum]['H-050'])-1.528*float(abstract_value[smilenum]['R5v'])-0.015*float(abstract_value[smilenum]['T(O..Cl)'])+ \
            0.043*float(abstract_value[smilenum]['HATS5v'])-0.026*float(abstract_value[smilenum]['RDF035m'])-0.197*float(abstract_value[smilenum]['RCI'])- \
            0.130*float(abstract_value[smilenum]['nRCOOR'])-0.077*float(abstract_value[smilenum]['Mor15u'])-0.077*float(abstract_value[smilenum]['RDF090m'])
    def logRP(self, para,d):
        '''
        logRP model computation
        '''
        abstract_value = d.extractparameter(["TDB05v", "Hypnotic-80"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logRP'] = -11.5+16.6*float(abstract_value[smilenum]['TDB05v'])+1.81*float(abstract_value[smilenum]['Hypnotic-80'])
    
MODEL_FOR_COMPUTAIONCLASS = {}
MODEL_FOR_COMPUTAIONCLASS["logKOA"] =  PredictionModel_ForParamInDragon
MODEL_FOR_COMPUTAIONCLASS["logRP"]  =  PredictionModel_ForParamInDragon
class PredictionModel(object):
    def __init__(self, modelnames=None, para={}):
        modelnames = modelnames or []
        predictionclass = {}
        #1:put all computation-needed prediction models name into predictionclass
        #the key of predictionclass is different computation models 
        #and the value is models'name list
        for modelname in modelnames:
            if not predictionclass.has_key(MODEL_FOR_COMPUTAIONCLASS[modelname]):
                predictionclass[MODEL_FOR_COMPUTAIONCLASS[modelname]] = []
            predictionclass[MODEL_FOR_COMPUTAIONCLASS[modelname]].append(modelname)
        #2:start to initiate different computation models 
        for prediction_model in predictionclass.keys():
            prediction_model(predictionclass[prediction_model], para)
'''            
para ={
    "smilestring":"c1ccccc1C(=O)c1cc(c(cc1O)OC)S(=O)(=O)O,c1(ccc(cc1)OC)/C=C/C(=O)OCCOCC",
    "filename"   :"",
    "cas"        :"",
       }  
pm = PredictionModel(["logKOA", "logRP"], para)
'''
