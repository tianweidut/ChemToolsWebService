# coding: utf-8
from numpy import matrix, linalg
import math
from collections import defaultdict

from .dragon import DragonModel
from chemistry.calcore.utils import fetch_polarizability, convert_stand_t, fetch_ehomo
from utils import chemistry_logger


class PredictionModel(object):
    def __init__(self, model_name=None,
                 smile=None, mol_fpath=None,
                 T=25):
        self.predict_result = {}
        self.T = convert_stand_t(T)

        if self.T == 0 and model_name in ('logKOA', 'logKOH_T'):
            raise Exception('The T of KOA or KOH_T can not be 0')

        self.dragon_model = DragonModel(model_name, smile, mol_fpath)

    def round(self, value):
        value = float(value)
        return round(value, 4)

    def calculate(self, modelname):
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
        from .matrix.koa import koaX

        #KOA 有温度参数
        #X1sol Mor13v H050 R5v TO..Cl HATS5v RDF035m RCl nRCOOR Mor15u RDF90m 1/T
        abstract_value = self.dragon_model.extractparameter([
            "X1sol", "Mor13v", "H-050", "R5v",
            "T(O..Cl)", "HATS5v", "RDF035m",
            "RCI", "nRCOOR", "Mor15u",
            "RDF090m"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = defaultdict(dict)

            value = -3.03 + \
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

            self.predict_result[smilenum]['logKOA']['value'] = self.round(value)
            chemistry_logger.info('koa(%s) dragon: %s' % (smilenum, abstract_value[smilenum]))

            x = matrix([[abstract_value[smilenum]['X1sol'],
                         abstract_value[smilenum]['Mor13v'],
                         abstract_value[smilenum]['H-050'],
                         abstract_value[smilenum]['R5v'],
                         abstract_value[smilenum]['T(O..Cl)'],
                         abstract_value[smilenum]['HATS5v'],
                         abstract_value[smilenum]['RDF035m'],
                         abstract_value[smilenum]['RCI'],
                         abstract_value[smilenum]['nRCOOR'],
                         abstract_value[smilenum]['Mor15u'],
                         abstract_value[smilenum]['RDF090m'],
                         1.0 / self.T,
                         ]])
            williams = self.get_williams(koaX, x)
            self.predict_result[smilenum]['logKOA'].update(williams)

    def logRP(self):
        #RP 无温度参数
        from .matrix.rp1 import rp1X
        #rp1: CAS nArOH CIC3 Eig15_EA(dm) H7m RTs+
        from .matrix.rp2 import rp2X
        #rp2: CAS H2s Mor07m R8v+

        ab = self.dragon_model.extractparameter([
            'nN', 'nCar', 'nArOH', 'nArCOOH', 'nROH',
            'nRCOOH', 'nSO2OH', 'nSOOH', 'nArX', 'nX',
            'H2s', 'Mor07m', 'R8v+', 'CIC3', 'Eig15_EA(dm)',
            'H7m', 'RTs+'])

        for s in ab.keys():
            if s not in self.predict_result:
                self.predict_result[s] = defaultdict(dict)

            cap_v = ab[s]['nROH'] + ab[s]['nRCOOH'] + ab[s]['nSO2OH'] + ab[s]['nSOOH']

            if ((ab[s]['nCar'] == 0 and cap_v == 0 and ab[s]['nX'] >= 0) or
                    (ab[s]['nCar'] == 0 and cap_v > 0)):
                # 模型2
                value = -4.279 + \
                    3.891 * 0.01 * ab[s]['H2s'] - \
                    1.961 * 0.1 * ab[s]['Mor07m'] + \
                    5.476 * 10 * ab[s]['R8v+']

                self.predict_result[s]['logRP']['value'] = self.round(value)
                x = matrix([[ab[s]['H2s'],
                             ab[s]['Mor07m'],
                             ab[s]['R8v+']]])
                williams = self.get_williams(rp2X, x)
            else:
                # 模型1
                value = -3.181 + \
                    2.515 * ab[s]['nArOH'] - \
                    8.990 * 0.1 * ab[s]['CIC3'] + \
                    3.463 * ab[s]['Eig15_EA(dm)'] + \
                    2.723 * 0.1 * ab[s]['H7m'] + \
                    6.901 * 0.1 * ab[s]['RTs+']

                self.predict_result[s]['logRP']['value'] = self.round(value)
                x = matrix([[ab[s]['nArOH'],
                             ab[s]['CIC3'],
                             ab[s]['Eig15_EA(dm)'],
                             ab[s]['H7m'],
                             ab[s]['RTs+']]])
                williams = self.get_williams(rp1X, x)

            self.predict_result[s]['logRP']['nN'] = ab[s]['nN']
            self.predict_result[s]['logRP'].update(williams)

    def logBCF(self):
        from .matrix.bcf import bcfX
        #BCF 无温度参数
        #CAS NO. MLOGP2 F02[C-Cl] nROH P-117 Mor25m N% X4v O-058 LLS_01 H4v SM12_AEA(dm) O-057
        abstract_value = self.dragon_model.extractparameter([
            "MLOGP2", "F02[C-Cl]", "nROH",
            "P-117", "Mor25m", "N%", "X4v",
            "O-058", "LLS_01", "H4v", "SM12_AEA(dm)", "O-057"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = defaultdict(dict)
            value = 2.137 + \
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
            
            self.predict_result[smilenum]['logBCF']['value'] = self.round(value)

            chemistry_logger.info('bcf(%s) dragon: %s' % (smilenum, abstract_value[smilenum]))

            x = matrix([[abstract_value[smilenum]['MLOGP2'],
                         abstract_value[smilenum]['F02[C-Cl]'],
                         abstract_value[smilenum]['nROH'],
                         abstract_value[smilenum]['P-117'],
                         abstract_value[smilenum]['Mor25m'],
                         abstract_value[smilenum]['N%'],
                         abstract_value[smilenum]['X4v'],
                         abstract_value[smilenum]['O-058'],
                         abstract_value[smilenum]['LLS_01'],
                         abstract_value[smilenum]['H4v'],
                         abstract_value[smilenum]['SM12_AEA(dm)'],
                         abstract_value[smilenum]['O-057']]])
            williams = self.get_williams(bcfX, x)
            self.predict_result[smilenum]['logBCF'].update(williams)

    def logKOH(self):
        from .matrix.koh_298k import koh_298kX
        # KOH 298K预测模型, 无温度参数
        #CAS-Number EHOMO AMW NdsCH Mor14i nP nR=Cp X% nRCHO C-020 SpMaxA_AEA(dm) nCbH CATS2D_03_DL
        abstract_value = self.dragon_model.extractparameter([
            "EHOMO", "AMW", "NdsCH", "Mor14i", "nP", "nR=Cp",
            "X%", "nRCHO", "C-020", "SpMaxA_AEA(dm)",
            "nCbH", "CATS2D_03_DL"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = defaultdict(dict)

            abstract_value[smilenum]['EHOMO'] = fetch_ehomo(smilenum, 'logKOH')
            
            value = -6.511 + \
                15.85 * abstract_value[smilenum]['EHOMO'] - \
                0.03800 * abstract_value[smilenum]['AMW'] + \
                0.1300 * abstract_value[smilenum]['NdsCH'] + \
                0.1630 * abstract_value[smilenum]['Mor14i'] + \
                0.7790 * abstract_value[smilenum]['nP'] + \
                0.3170 * abstract_value[smilenum]['nR=Cp'] - \
                0.01900 * abstract_value[smilenum]['X%'] + \
                0.3930 * abstract_value[smilenum]['nRCHO'] + \
                0.5890 * abstract_value[smilenum]['C-020'] - \
                0.4550 * abstract_value[smilenum]['SpMaxA_AEA(dm)'] - \
                0.05600 * abstract_value[smilenum]['nCbH'] + \
                0.1410 * abstract_value[smilenum]['CATS2D_03_DL']
            
            self.predict_result[smilenum]['logKOH']['value'] = self.round(value)

            chemistry_logger.info('koh(%s) dragon: %s' % (smilenum, abstract_value[smilenum]))

            x = matrix([[abstract_value[smilenum]['EHOMO'],
                         abstract_value[smilenum]['AMW'],
                         abstract_value[smilenum]['NdsCH'],
                         abstract_value[smilenum]['Mor14i'],
                         abstract_value[smilenum]['nP'],
                         abstract_value[smilenum]['nR=Cp'],
                         abstract_value[smilenum]['X%'],
                         abstract_value[smilenum]['nRCHO'],
                         abstract_value[smilenum]['C-020'],
                         abstract_value[smilenum]['SpMaxA_AEA(dm)'],
                         abstract_value[smilenum]['nCbH'],
                         abstract_value[smilenum]['CATS2D_03_DL']]])
            williams = self.get_williams(koh_298kX, x)
            self.predict_result[smilenum]['logKOH'].update(williams)

    def logKOH_T(self):
        from .matrix.koh import kohX
        # KOH 温度依附性模型, 有温度参数
        #CAS-Number X% EHOMO Mor29u NdsCH GATS1e X3A 1/T SdsCH nR=Cp F02[F-Br] RDF015m BIC1 SpMin8_Bh(p) NssssC
        abstract_value = self.dragon_model.extractparameter([
            "X%", "EHOMO", "Mor29u", "NdsCH", "GATS1e", "X3A", "SdsCH",
            "nR=Cp", "F02[F-Br]", "RDF015m", "BIC1", "SpMin8_Bh(p)", "NssssC"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = defaultdict(dict)

            abstract_value[smilenum]['EHOMO'] = fetch_ehomo(smilenum, 'logKOH_T')

            value = -8.613 - \
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
            
            self.predict_result[smilenum]['logKOH_T']['value'] = self.round(value)

            chemistry_logger.info('koh_t(%s) dragon: %s' % (smilenum, abstract_value[smilenum]))

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
            williams = self.get_williams(kohX, x)
            self.predict_result[smilenum]['logKOH_T'].update(williams)

    def logKOC(self):
        from .matrix.koc import kocX
        # KOC 使用g09，无温度参数
        #CAS No. nN ATSC8v SpMaxA_G/D Mor16u nROH O-058 P-117 MLOGP2 Molecular Polarizability
        abstract_value = self.dragon_model.extractparameter([
            "nN", "ATSC8v", "SpMaxA_G/D", "Mor16u", "nROH",
            "O-058", "P-117", "MLOGP2", "α"])

        for smilenum in abstract_value:
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = defaultdict(dict)

            abstract_value[smilenum]['α'] = fetch_polarizability(smilenum, 'logKOC')
            value = -1.612 + \
                0.039 * abstract_value[smilenum]['MLOGP2'] +\
                0.010 * abstract_value[smilenum]["α"] -\
                0.342 * abstract_value[smilenum]['O-058'] -\
                0.069 * abstract_value[smilenum]['ATSC8v'] -\
                0.123 * abstract_value[smilenum]['nN'] -\
                0.368 * abstract_value[smilenum]['nROH'] -\
                0.473 * abstract_value[smilenum]['P-117'] +\
                2.335 * abstract_value[smilenum]['SpMaxA_G/D'] +\
                0.302 * abstract_value[smilenum]['Mor16u']

            self.predict_result[smilenum]['logKOC']['value'] = self.round(value)
            chemistry_logger.info('koc(%s) dragon: %s' % (smilenum, abstract_value[smilenum]))

            x = matrix([[abstract_value[smilenum]['nN'],
                         abstract_value[smilenum]['ATSC8v'],
                         abstract_value[smilenum]['SpMaxA_G/D'],
                         abstract_value[smilenum]['Mor16u'],
                         abstract_value[smilenum]['nROH'],
                         abstract_value[smilenum]['O-058'],
                         abstract_value[smilenum]['P-117'],
                         abstract_value[smilenum]['MLOGP2'],
                         abstract_value[smilenum]["α"]]])

            williams = self.get_williams(kocX, x)
            self.predict_result[smilenum]['logKOC'].update(williams)

    def logBDG(self):
        from .matrix.bdg import bdgX
        # BDG 无温度参数
        #CAS nN nHM O% MATS1e GATS1p GATS7p GGI1 GGI2 nCq nCrt C-040 H-048 H-051 O-059
        abstract_value = self.dragon_model.extractparameter([
            "nN", "nHM", "O%", "MATS1e", "GATS1p", "GATS7p", "GGI1", "GGI2",
            "nCq", "nCrt", "C-040", "H-048", "H-051", "O-059"])

        for smilenum in abstract_value.keys():
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = defaultdict(dict)

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
            
            self.predict_result[smilenum]['logBDG']['value'] = self.round(x)
            chemistry_logger.info('bdg(%s) dragon: %s' % (smilenum, abstract_value[smilenum]))
            #self.predict_result[smilenum]['logBDG']['value'] = self.round(1 / (1 + math.exp(-x)))

            x = matrix([[abstract_value[smilenum]['nN'],
                         abstract_value[smilenum]['nHM'],
                         abstract_value[smilenum]['O%'],
                         abstract_value[smilenum]['MATS1e'],
                         abstract_value[smilenum]['GATS1p'],
                         abstract_value[smilenum]['GATS7p'],
                         abstract_value[smilenum]['GGI1'],
                         abstract_value[smilenum]['GGI2'],
                         abstract_value[smilenum]['nCq'],
                         abstract_value[smilenum]['nCrt'],
                         abstract_value[smilenum]['C-040'],
                         abstract_value[smilenum]['H-048'],
                         abstract_value[smilenum]['H-051'],
                         abstract_value[smilenum]['O-059']]])

            williams = self.get_williams(bdgX, x)
            self.predict_result[smilenum]['logBDG'].update(williams)

    def logPL(self):
        from .matrix.pl import plX
        #PL 模型，有温度参数
        #CAS-Number 1/T nHDon X1sol GATS1v μ nROH
        abstract_value = self.dragon_model.extractparameter([
            "nHDon", "X1sol", "GATS1v", "μ", "nROH"])
        for smilenum in abstract_value.keys():
            if smilenum not in self.predict_result:
                self.predict_result[smilenum] = defaultdict(dict)
            value = 13.33 - \
                2571.0 * (1 / self.T) - \
                0.5061 * abstract_value[smilenum]['nHDon'] - \
                0.6896 * abstract_value[smilenum]['X1sol'] + \
                0.8014 * abstract_value[smilenum]['GATS1v'] - \
                0.1363 * abstract_value[smilenum]['μ'] - \
                0.6094 * abstract_value[smilenum]['nROH']

            self.predict_result[smilenum]['logPL']['value'] = self.round(value)
            chemistry_logger.info('pl(%s) dragon: %s' % (smilenum, abstract_value[smilenum]))

            x = matrix([[(1 / self.T),
                         abstract_value[smilenum]['nHDon'],
                         abstract_value[smilenum]['X1sol'],
                         abstract_value[smilenum]['GATS1v'],
                         abstract_value[smilenum]['μ'],
                         abstract_value[smilenum]['nROH']]])
            williams = self.get_williams(plX, x)
            self.predict_result[smilenum]['logPL'].update(williams)

    def get_williams(self, X, x):
        return dict(hx=3 * (X.shape[1] + 1.0) / X.shape[0],
                    hi=(x * linalg.inv(X.T * X) * x.T)[0, 0])


def prediction_model_calculate(model_name, smile, mol_fpath, temperature):
    pm = PredictionModel(model_name, smile, mol_fpath, T=temperature)
    pm.calculate(model_name)
    chemistry_logger.info("pm result:%s", pm.predict_result)
    return pm.predict_result
