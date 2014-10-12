# coding: utf-8
from numpy import matrix, linalg
import math

from .dragon import DragonModel
from .train_matrix import kocX, koh_TX
from utils import chemistry_logger


class PredictionModel(object):
    def __init__(self, model_name=None,
                 smile=None, mol_fpath=None,
                 T=None, hi=None, hx=None):
        self.predict_result = {}
        self.hi = hi
        self.hx = hx
        self.T = T

        if self.T == 0 and model_name in ('logKOA', 'logKOH_T'):
            raise Exception('The T of KOA or KOH_T can not be 0')

        self.dragon_model = DragonModel(model_name, smile, mol_fpath)
        self.dragon_model.mol2drs()

        self.predict_result["invalidnums"] = self.dragon_model.invalidnums
        self.models_computation(model_name)

    def models_computation(self, modelname):
        {
            "logKOA": self.logKOA,
            "logRP": self.logRP,
            "logKOC": self.logKOC,
            "logBCF": self.logBCF,
            "logKOH": self.logKOH,
            "logKOH_T": self.logKOH_T,
            "logPL": self.logPL,
            "logBDG": self.logBDG,
        }[modelname]()

    def logKOA(self):
        #KOA 有温度参数
        abstract_value = self.dragon_model.extractparameter([
            "X1sol", "Mor13v", "HATS5v", "RDF035m", "Mor15u",
            "RDF090m", "H-050", "nRCOOR", "R5v", "T(O..Cl)",
            "RCI", "nRCOOR"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}

            self.predict_result[smilenum]['logKOA'] = -3.03 + \
                313.0 * abstract_value[smilenum]['X1sol'] / self.T - \
                85.7 * abstract_value[smilenum]['Mor13v'] / self.T + \
                432.0 * abstract_value[smilenum]['H-050'] / self.T - \
                1270.0 * abstract_value[smilenum]['R5v'] / self.T - \
                5.54 * abstract_value[smilenum]['T(O..Cl)'] / self.T + \
                125.0 * abstract_value[smilenum]['HATS5v'] / self.T - \
                13.3 * abstract_value[smilenum]['RDF035m'] / self.T - \
                61.1 * abstract_value[smilenum]['RCI'] / self.T - \
                37.6 * abstract_value[smilenum]['nRCOOR'] / self.T + \
                156.0 * abstract_value[smilenum]['Mor15u'] / self.T -\
                5.49 * abstract_value[smilenum]['RDF090m'] / self.T + \
                1040.0 / self.T

    def logRP(self):
        #RP 无温度参数
        abstract_value = self.dragon_model.extractparameter([
            "TDB05v", "Hypnotic-80"])

        for smilenum in abstract_value.keys():
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}

            self.predict_result[smilenum]['logRP'] = -11.857 + 18.968 * \
                abstract_value[smilenum]['TDB05v'] + 1.480 * \
                abstract_value[smilenum]['Hypnotic-80']

    def logBCF(self):
        #BCF 无温度参数
        abstract_value = self.dragon_model.extractparameter([
            "MLOGP2", "F02[C-Cl]", "nROH", "P-117", "Mor25m",
            "N%", "X4v", "O-058", "LLS_01", "H4v", "SM12_AEA(dm)", "O-057"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logBCF'] = 2.137 + \
                0.061 * abstract_value[smilenum]['MLOGP2'] + \
                0.034 * abstract_value[smilenum]['F02[C-Cl]'] - \
                0.312 * abstract_value[smilenum]['nROH'] - \
                1.282 * abstract_value[smilenum]['P-117'] + \
                0.323 * abstract_value[smilenum]['Mor25m'] - \
                0.052 * abstract_value[smilenum]['N%'] + \
                0.080 * abstract_value[smilenum]['X4v'] - \
                0.289 * abstract_value[smilenum]['O-058'] - \
                1.137 * abstract_value[smilenum]['LLS_01'] - \
                1.387 * abstract_value[smilenum]['H4v'] + \
                0.071 * abstract_value[smilenum]['SM12_AEA(dm)'] - \
                0.269 * abstract_value[smilenum]['O-057']

    def logKOH(self):
        # KOH 298K预测模型, 无温度参数
        abstract_value = self.dragon_model.extractparameter([
            "EHOMO", "AMW", "NdsCH", "Mor14i", "nR=Cp",
            "nP", "nRCHO", "X%", "SpMaxA_AEA(dm)", "C-020",
            "nCbH", "CATS2D_03_DL"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logKOH'] = -6.511 + \
                15.85 * abstract_value[smilenum]['EHOMO'] - \
                0.03800 * abstract_value[smilenum]['AMW'] + \
                0.1300 * abstract_value[smilenum]['NdsCH'] + \
                0.1630 * abstract_value[smilenum]['Mor14i'] + \
                0.3170 * abstract_value[smilenum]['nR=Cp'] + \
                0.7790 * abstract_value[smilenum]['nP'] + \
                0.3930 * abstract_value[smilenum]['nRCHO'] - \
                0.01900 * abstract_value[smilenum]['X%'] - \
                0.4550 * abstract_value[smilenum]['SpMaxA_AEA(dm)'] + \
                0.5890 * abstract_value[smilenum]['C-020'] - \
                0.05600 * abstract_value[smilenum]['nCbH'] + \
                0.1410 * abstract_value[smilenum]['CATS2D_03_DL']

    def logKOH_T(self):
        # KOH 温度依附性模型, 有温度参数
        abstract_value = self.dragon_model.extractparameter([
            "EHOMO", "X%", "Mor29u", "NdsCH", "GATS1e", "X3A", "SdsCH",
            "BIC1", "RDF015m", "SpMin8_Bh(p)", "nR=Cp", "NssssC", "F02[F-Br]"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logKOH_T'] = -8.613 - \
                0.02100 * abstract_value[smilenum]['X%'] + \
                14.38 * abstract_value[smilenum]['EHOMO'] - \
                0.6430 * abstract_value[smilenum]['Mor29u'] + \
                0.5870 * abstract_value[smilenum]['NdsCH'] + \
                0.5870 * abstract_value[smilenum]['GATS1e'] + \
                0.5770 * abstract_value[smilenum]['X3A'] - \
                0.2450 * abstract_value[smilenum]['SdsCH'] - \
                167.0 * (1 / self.T) + \
                1.103 * abstract_value[smilenum]['BIC1'] + \
                0.1170 * abstract_value[smilenum]['RDF015m'] - \
                1.044 * abstract_value[smilenum]['SpMin8_Bh(p)'] + \
                0.2390 * abstract_value[smilenum]['nR=Cp'] - \
                0.1980 * abstract_value[smilenum]['NssssC'] - \
                0.5080 * abstract_value[smilenum]['F02[F-Br]']

        x = matrix([[abstract_value[smilenum]['X%'],
                     abstract_value[smilenum]['EHOMO'],
                     abstract_value[smilenum]['Mor29u'],
                     abstract_value[smilenum]['NdsCH'],
                     abstract_value[smilenum]['GATS1e'],
                     abstract_value[smilenum]['X3A'],
                     1.0 / self.T,
                     abstract_value[smilenum]['SdsCH'],
                     abstract_value[smilenum]['nR=Cp'],
                     abstract_value[smilenum]['F02[F-Br]'],
                     abstract_value[smilenum]['RDF015m'],
                     abstract_value[smilenum]['BIC1'],
                     abstract_value[smilenum]['SpMin8_Bh(p)'],
                     abstract_value[smilenum]['NssssC']
                     ]])
        self.Williams(koh_TX, x)

    def logKOC(self):
        # KOC 使用g09，无温度参数
        abstract_value = self.dragon_model.extractparameter([
            "MLOGP2", "WiA_Dt", "H_D/Dt", "nHM", "O-061", "HATS4v",
            "P-117", "nR=CRX", "F05[N-O]", "B08[Br-Br]", "R3e+",
            "B03[N-S]", "CATS2D_05_NL", "F02[S-S]", "nRCN"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logKOC'] = 0.546 + \
                0.063 * abstract_value[smilenum]['MLOGP2'] + \
                0.332 * abstract_value[smilenum]['WiA_Dt'] + \
                0.260 * abstract_value[smilenum]['nHM'] - \
                0.002 * abstract_value[smilenum]['H_D/Dt'] + \
                0.338 * abstract_value[smilenum]['O-061'] - \
                1.037 * abstract_value[smilenum]['HATS4v'] - \
                0.803 * abstract_value[smilenum]['P-117'] + \
                1.011 * abstract_value[smilenum]['nR=CRX'] - \
                0.123 * abstract_value[smilenum]['F05[N-O]'] + \
                1.185 * abstract_value[smilenum]['B08[Br-Br]'] - \
                1.868 * abstract_value[smilenum]['R3e+'] - \
                0.537 * abstract_value[smilenum]['B03[N-S]'] - \
                0.227 * abstract_value[smilenum]['CATS2D_05_NL'] + \
                0.220 * abstract_value[smilenum]['F02[S-S]'] + \
                0.627 * abstract_value[smilenum]['nRCN']

        x = matrix([[abstract_value[smilenum]['nHM'],
                     abstract_value[smilenum]['WiA_Dt'],
                     abstract_value[smilenum]['H_D/Dt'],
                     abstract_value[smilenum]['HATS4v'],
                     abstract_value[smilenum]['R3e+'],
                     abstract_value[smilenum]['nRCN'],
                     abstract_value[smilenum]['nR=CRX'],
                     abstract_value[smilenum]['O-061'],
                     abstract_value[smilenum]['P-117'],
                     abstract_value[smilenum]['CATS2D_05_NL'],
                     abstract_value[smilenum]['B03[N-S]'],
                     abstract_value[smilenum]['B08[Br-Br]'],
                     abstract_value[smilenum]['F02[S-S]'],
                     abstract_value[smilenum]['F05[N-O]'],
                     abstract_value[smilenum]['MLOGP2']
                     ]])
        self.Williams(kocX, x)

    def logBDG(self):
        # BDG 无温度参数
        abstract_value = self.dragon_model.extractparameter([
            "nN", "nHM", "O%", "MATS1e", "GATS1p", "GATS7p", "GGI1", "GGI2",
            "nCq", "nCrt", "C-040", "H-048", "H-051", "O-059"])

        for smilenum in abstract_value.keys():
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}
                x = 1.9025 + \
                    1.0457 * abstract_value[smilenum]['nN'] + \
                    0.6662 * abstract_value[smilenum]['nHM'] - \
                    0.1078 * abstract_value[smilenum]['O%'] + \
                    2.8362 * abstract_value[smilenum]['MATS1e'] - \
                    2.0019 * abstract_value[smilenum]['GATS1p'] - \
                    0.7015 * abstract_value[smilenum]['GATS7p'] + \
                    0.1131 * abstract_value[smilenum]['GGI1'] + \
                    0.7023 * abstract_value[smilenum]['GGI2'] + \
                    2.7793 * abstract_value[smilenum]['nCq'] + \
                    1.035 * abstract_value[smilenum]['nCrt'] - \
                    0.777 * abstract_value[smilenum]['C-040'] - \
                    0.7091 * abstract_value[smilenum]['H-048'] - \
                    0.1553 * abstract_value[smilenum]['H-051'] + \
                    0.955 * abstract_value[smilenum]['O-059']
                self.predict_result[smilenum]['logBDG'] = 1 / (1 + math.exp(-x))

    def logPL(self):
        #PL 模型，有温度参数
        abstract_value = self.dragon_model.extractparameter([
            "nHDon", "X1sol", "nROH", "u", "GATS1v"])
        for smilenum in abstract_value.keys():
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = {}
            self.predict_result[smilenum]['logPL'] = 13.33 - \
                2571.0 * (1 / self.T) - \
                0.5061 * abstract_value[smilenum]['nHDon'] - \
                0.6896 * abstract_value[smilenum]['X1sol'] + \
                0.8014 * abstract_value[smilenum]['GATS1v'] - \
                0.1363 * abstract_value[smilenum]['u'] - \
                0.6094 * abstract_value[smilenum]['nROH']

    def Williams(self, X, x):
        self.hx = 3 * (X.shape[1] + 1.0) / X.shape[0]
        self.hi = (x * linalg.inv(X.T * X) * x.T)[0, 0]


def prediction_model_calculate(model_name, smile, mol_fpath, temperature):
    pm = PredictionModel(model_name, smile, mol_fpath, T=temperature)
    chemistry_logger.info("pm result:%s", pm.predict_result)
    return pm.predict_result
