'''
Created on 2012-12-4

@author: SongYang
'''
from calcore.controllers.Dragon import Dragon
from numpy import *
from calcore.controllers.train_matrix import *
class PredictionModel_ForParamInDragon(object):
    '''
this class is used for model computation that parameters needed in Dragon output file
    '''
    def __init__(self,modelname=None,para={},predict_results=None,molpath={},T=None,hi=None,hx=None):
        self.predict_result = predict_results
        self.hi=hi
        self.hx=hx
        self.T=T
        if self.T==0:
            raise Exception,'The T of KOA or KOH_T can not be 0'
        #self.model_type={}
        para = para or {}
        print "in the PredictionModel_ForParamInDragon"
        #start to compute model  results
        print modelname[0]
        print self.get_ModelType(modelname[0])
        #print self.model_type 
        d = Dragon(smiles_str=para["smilestring"],
                molfile=para["filename"],molpath=molpath,modeltype=self.get_ModelType(modelname[0]))
        d.mol2drs()
        self.predict_result["invalidnums"] = d.invalidnums
        modelname = modelname or []
        for name in modelname:
            self.models_computation(name, para ,d)
        print self.predict_result
        print "--------------------------------------------------"
#print the model results
    def get_ModelType(self,modelname=None):
        modeltype={}
        if modelname=="logKOA" or modelname=="logRP":
            modeltype=1
        elif modelname=="logKOC" or modelname=="logBCF":
            #self.model_type=2
            modeltype=2
        elif modelname=="logKOH" or modelname=="logKOH_T":
            modeltype=3
        else: 
            modeltype=0
        return modeltype

    def models_computation(self, modelname, para ,instance_of_dragon):
                    {
         "logKOA" :  lambda para:self.logKOA(para ,instance_of_dragon),
         "logRP"  :  lambda para:self.logRP(para ,instance_of_dragon),
         "logKOC" :  lambda para:self.logKOC(para ,instance_of_dragon),
         "logBCF" :  lambda para:self.logBCF(para,instance_of_dragon),
         "logKOH" :  lambda para:self.logKOH(para,instance_of_dragon),
         "logKOH_T": lambda para:self.logKOH_T(para,instance_of_dragon),
         
        }[modelname](para)
    def logKOA(self, para ,d):
        '''
        logKOA model computation
        '''
        abstract_value = d.extractparameter(["X1sol", "Mor13v", "HATS5v", "RDF035m","Mor15u" ,"RDF090m", "H-050", "nRCOOR", "R5v", "T(O..Cl)", "RCI","nRCOOR"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logKOA']=-3.03+313*float(abstract_value[smilenum]['X1sol'])/(self.T)-85.7*float(abstract_value[smilenum]['Mor13v'])/(self.T)+ \
            432*float(abstract_value[smilenum]['H-050'])/(self.T)-1270*float(abstract_value[smilenum]['R5v'])/(self.T)-5.54*float(abstract_value[smilenum]['T(O..Cl)'])/(self.T)+ \
            125*float(abstract_value[smilenum]['HATS5v'])/(self.T)-13.3*float(abstract_value[smilenum]['RDF035m'])/(self.T)-61.1*float(abstract_value[smilenum]['RCI'])/(self.T)- \
            37.6*float(abstract_value[smilenum]['nRCOOR'])/(self.T)-156*float(abstract_value[smilenum]['Mor15u'])/(self.T)-5.49*float(abstract_value[smilenum]['RDF090m'])/(self.T)+1040.0/(self.T)
        print self.T
        print 'X1sol',float(abstract_value[smilenum]['X1sol'])/(self.T),"Mor13v",float(abstract_value[smilenum]['Mor13v'])/(self.T),"H_050",float(abstract_value[smilenum]['H-050'])/(self.T),"R5v",float(abstract_value[smilenum]['R5v'])/(self.T),"T(O..Cl)",float(abstract_value[smilenum]['T(O..Cl)'])/(self.T),"HATS5v",float(abstract_value[smilenum]['HATS5v'])/(self.T),"RDF035m",float(abstract_value[smilenum]['RDF035m'])/(self.T),"RCI",float(abstract_value[smilenum]['RCI'])/(self.T),"nRCOOR",float(abstract_value[smilenum]['nRCOOR'])/(self.T),"Mor15u",float(abstract_value[smilenum]['Mor15u'])/(self.T),"RDF090m",float(abstract_value[smilenum]['RDF090m'])/(self.T)
    def logRP(self, para,d):
        '''
        logRP model computation
        '''
        abstract_value =d.extractparameter(["TDB05v", "Hypnotic-80"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logRP'] =-11.857+18.968*float(abstract_value[smilenum]['TDB05v'])+1.480*float(abstract_value[smilenum]['Hypnotic-80'])
    def logBCF(self, para,d):
        '''
        logBCF model computation
        '''
        abstract_value =d.extractparameter(["MLOGP2","F02[C-Cl]","nROH","P-117","Mor25m","N%","X4v","O-058","LLS_01","H4v","SM12_AEA(dm)","O-057"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logBCF']=2.137+0.061*float(abstract_value[smilenum]['MLOGP2'])+0.034*float(abstract_value[smilenum]['F02[C-Cl]'])- \
            0.312*float(abstract_value[smilenum]['nROH'])-1.282*float(abstract_value[smilenum]['P-117'])+0.323*float(abstract_value[smilenum]['Mor25m'])- \
            0.052*float(abstract_value[smilenum]['N%'])+0.080*float(abstract_value[smilenum]['X4v'])-0.289*float(abstract_value[smilenum]['O-058'])- \
            1.137*float(abstract_value[smilenum]['LLS_01'])-1.387*float(abstract_value[smilenum]['H4v'])+0.071*float(abstract_value[smilenum]['SM12_AEA(dm)'])-0.269*float(abstract_value[smilenum]['O-057'])
            #print float(abstract_value[smilenum]['MLOGP2']),float(abstract_value[smilenum]['F02[C-Cl]']),float(abstract_value[smilenum]['nROH']),float(abstract_value[smilenum]['P-117']),float(abstract_value[smilenum]['Mor25m']),float(abstract_value[smilenum]['N%']),float(abstract_value[smilenum]['X4v']),float(abstract_value[smilenum]['O-058']),float(abstract_value[smilenum]['LLS_01']),float(abstract_value[smilenum]['H4v']),float(abstract_value[smilenum]['SM12_AEA(dm)']),float(abstract_value[smilenum]['O-057'])
    def logKOH(self,para,d):
        '''
        logKOH model with T=298K
        '''
        abstract_value=d.extractparameter(["EHOMO","AMW","NdsCH","Mor14i","nR=Cp","nP","nRCHO","X%","SpMaxA_AEA(dm)","C-020","nCbH","CATS2D_03_DL"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logKOH']=-6.511+15.85*float(abstract_value[smilenum]['EHOMO'])-0.03800*float(abstract_value[smilenum]['AMW'])+ \
            0.1300*float(abstract_value[smilenum]['NdsCH'])+0.1630*float(abstract_value[smilenum]['Mor14i'])+0.3170*float(abstract_value[smilenum]['nR=Cp'])+ \
            0.7790*float(abstract_value[smilenum]['nP'])+0.3930*float(abstract_value[smilenum]['nRCHO'])-0.01900*float(abstract_value[smilenum]['X%'])- \
            0.4550*float(abstract_value[smilenum]['SpMaxA_AEA(dm)'])+0.5890*float(abstract_value[smilenum]['C-020'])-0.05600*float(abstract_value[smilenum]['nCbH'])+ \
            0.1410*float(abstract_value[smilenum]['CATS2D_03_DL'])
            print float(abstract_value[smilenum]['EHOMO'])
    def logKOH_T(self,para,d):
        '''
        logKOH_T model with T=TK
        '''
        abstract_value=d.extractparameter(["EHOMO","X%","Mor29u","NdsCH","GATS1e","X3A","SdsCH","BIC1","RDF015m","SpMin8_Bh(p)","nR=Cp","NssssC","F02[F-Br]"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logKOH_T']=-8.613-0.02100*float(abstract_value[smilenum]['X%'])+14.38*float(abstract_value[smilenum]['EHOMO'])- \
            0.6430*float(abstract_value[smilenum]['Mor29u'])+0.5870*float(abstract_value[smilenum]['NdsCH'])+0.5870*float(abstract_value[smilenum]['GATS1e'])+ \
            0.5770*float(abstract_value[smilenum]['X3A'])-0.2450*float(abstract_value[smilenum]['SdsCH'])-167.0*(1/self.T)+1.103*float(abstract_value[smilenum]['BIC1'])+ \
            0.1170*float(abstract_value[smilenum]['RDF015m'])-1.044*float(abstract_value[smilenum]['SpMin8_Bh(p)'])+0.2390*float(abstract_value[smilenum]['nR=Cp'])-0.1980*float(abstract_value[smilenum]['NssssC'])-0.5080*float(abstract_value[smilenum]['F02[F-Br]'])
            print self.T
            
    def logKOC(self, para,d):
        '''
        logKOC model computation
        '''
        abstract_value=d.extractparameter(["MLOGP2","WiA_Dt","H_D/Dt","nHM","O-061","HATS4v","P-117","nR=CRX","F05[N-O]","B08[Br-Br]","R3e+","B03[N-S]","CATS2D_05_NL","F02[S-S]","nRCN"])
        for smilenum in abstract_value.keys():
            if not self.predict_result.has_key(smilenum):
                self.predict_result[smilenum]={}
            self.predict_result[smilenum]['logKOC']=0.063*float(abstract_value[smilenum]['MLOGP2'])+0.332*float(abstract_value[smilenum]['WiA_Dt'])+ \
            0.260*float(abstract_value[smilenum]['nHM'])-0.002*float(abstract_value[smilenum]['H_D/Dt'])+0.338*float(abstract_value[smilenum]['O-061'])- \
            1.037*float(abstract_value[smilenum]['HATS4v'])-0.803*float(abstract_value[smilenum]['P-117'])+1.011*float(abstract_value[smilenum]['nR=CRX'])- \
            0.123*float(abstract_value[smilenum]['F05[N-O]'])+1.185*float(abstract_value[smilenum]['B08[Br-Br]'])-1.868*float(abstract_value[smilenum]['R3e+'])- \
            0.537*float(abstract_value[smilenum]['B03[N-S]'])-0.227*float(abstract_value[smilenum]['CATS2D_05_NL'])+0.220*float(abstract_value[smilenum]['F02[S-S]'])+0.627*float(abstract_value[smilenum]['nRCN'])+0.546
        x=matrix([[float(abstract_value[smilenum]['nHM']),float(abstract_value[smilenum]['WiA_Dt']),float(abstract_value[smilenum]['H_D/Dt']),
            float(abstract_value[smilenum]['HATS4v']),float(abstract_value[smilenum]['R3e+']),float(abstract_value[smilenum]['nRCN']),
            float(abstract_value[smilenum]['nR=CRX']),float(abstract_value[smilenum]['O-061']),float(abstract_value[smilenum]['P-117']),
            float(abstract_value[smilenum]['CATS2D_05_NL']),float(abstract_value[smilenum]['B03[N-S]']),float(abstract_value[smilenum]['B08[Br-Br]']),
            float(abstract_value[smilenum]['F02[S-S]']),float(abstract_value[smilenum]['F05[N-O]']),float(abstract_value[smilenum]['MLOGP2'])]])
        print float(abstract_value[smilenum]['nHM']),float(abstract_value[smilenum]['WiA_Dt']),float(abstract_value[smilenum]['H_D/Dt']),float(abstract_value[smilenum]['HATS4v']),float(abstract_value[smilenum]['R3e+']),float(abstract_value[smilenum]['nRCN']),float(abstract_value[smilenum]['nR=CRX']),float(abstract_value[smilenum]['O-061']),float(abstract_value[smilenum]['P-117']),float(abstract_value[smilenum]['CATS2D_05_NL']),float(abstract_value[smilenum]['B03[N-S]']),float(abstract_value[smilenum]['B08[Br-Br]']),float(abstract_value[smilenum]['F02[S-S]']),float(abstract_value[smilenum]['F05[N-O]']),float(abstract_value[smilenum]['MLOGP2'])
        print kocX,x
        self.Williams(kocX,x)
        #print float(abstract_value[smilenum]['q+']),float(abstract_value[smilenum]['a'])   
    def Williams(self,X,x):
        self.hx=3*(X.shape[1]+1.0)/X.shape[0]
        self.hi=(x*linalg.inv(X.T*X)*x.T)[0,0]
        print self.hx,self.hi

MODEL_FOR_COMPUTAIONCLASS = {}
MODEL_FOR_COMPUTAIONCLASS["logKOA"] =  PredictionModel_ForParamInDragon
MODEL_FOR_COMPUTAIONCLASS["logRP"]  =  PredictionModel_ForParamInDragon
MODEL_FOR_COMPUTAIONCLASS["logKOC"] =  PredictionModel_ForParamInDragon
MODEL_FOR_COMPUTAIONCLASS["logBCF"] =  PredictionModel_ForParamInDragon
MODEL_FOR_COMPUTAIONCLASS["logKOH"] =  PredictionModel_ForParamInDragon
MODEL_FOR_COMPUTAIONCLASS["logKOH_T"]= PredictionModel_ForParamInDragon
class PredictionModel(object):
    def __init__(self, modelnames=None, para={}, molpath={},T=None):
        modelnames = modelnames or []
        predictionclass = {}
        self.predict_results={}
        #1:put all computation-needed prediction models name into predictionclass
        #the key of predictionclass is different computation models 
        #and the value is models'name list
        for modelname in modelnames:
            if not predictionclass.has_key(MODEL_FOR_COMPUTAIONCLASS[modelname]):
                predictionclass[MODEL_FOR_COMPUTAIONCLASS[modelname]] = []
            predictionclass[MODEL_FOR_COMPUTAIONCLASS[modelname]].append(modelname)
        #2:start to initiate different computation models 
        for prediction_model in predictionclass.keys():
            prediction_model(predictionclass[prediction_model],
                    para,self.predict_results,molpath,T)
'''            
para ={
    "smilestring":"c1ccccc1C(=O)c1cc(c(cc1O)OC)S(=O)(=O)O,c1(ccc(cc1)OC)/C=C/C(=O)OCCOCC",
    "filename"   :"",
    "cas"        :"",
       }  
pm = PredictionModel(["logKOA", "logRP"], para)
'''
