# coding: utf-8

from chemistry.calcore.prediciton_model import prediction_model_calculate


def calcore_validate():
    model = 'logKOA'
    smile = 'COc1ccccc1NC(=O)CC(=O)C'
    mol_path = '/home/vagrant/tianwei/ChemToolsWebService/media/tmp/process_file/89db0959-9742-418c-a5d4-1c2906c1c337.mol'
    temperature = 10.0

    r = prediction_model_calculate(model, smile, mol_path, temperature)
    print r
