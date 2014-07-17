# coding: utf-8

from chemistry.calcore.prediciton_model import prediction_model_calculate


def calcore_validate():
    model = 'logKOA'
    smile = 'COc1ccccc1NC(=O)CC(=O)C'
    mol_path = ''
    temperature = 10.0

    r = prediction_model_calculate(model, smile, mol_path, temperature)
    print r


def calcore_validate_model(model):
    smile = 'COc1ccccc1NC(=O)CC(=O)C'
    mol_path = ''
    temperature = 10.0

    r = prediction_model_calculate(model, smile, mol_path, temperature)
    print r
