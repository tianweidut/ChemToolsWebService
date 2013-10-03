#coding: utf-8
import os
import sys
import xlrd

from django.db import models
from django.conf import settings
from calcore.models import ChemInfoLocal

DATA_FILE = os.path.join(settings.SETTINGS_ROOT, 'deploy', "data.xls")
SHEET_NAME = "work"

CAS = 0
EINECS = 1
EINECS_Name = 2
EINECS_MF = 3
Frequency = 4
Num_PositiveAtoms = 5
Num_NegativeAtoms = 6
FormalCharge = 7
Num_H_Acceptors = 8
Num_H_Donors = 9
Molecular_Solubility = 10
ALogP = 11
LogD = 12
Molecular_Formula = 13
Canonical_Smiles = 14
InChI = 15
Molecular_SAVol = 16


def write_row_record(row, contents):
    cass = contents.cell(row, CAS).value.split(";")
    einecss = contents.cell(row, EINECS).value.split(";")
    einecs_names = contents.cell(row, EINECS_Name).value.split(";")
    einecs_mfs = contents.cell(row, EINECS_MF).value.split(";")

    if not (len(cass) == len(einecss) == len(einecs_names) == len(einecs_mfs)):
        if len(cass) == len(einecss) == len(einecs_mfs) == 1:
            einecs_names = (contents.cell(row, EINECS_Name).value,)
        else:
            raise Exception,(len(cass), len(einecss), len(einecs_names), len(einecs_mfs))

    for d in zip(cass, einecss, einecs_names, einecs_mfs):
        chem = ChemInfoLocal()
        chem.cas = d[0]
        chem.einecs = d[1]
        chem.einecs_name = d[2]
        chem.einecs_mf = d[3]
        chem.frequency = int(contents.cell(row, Frequency).value)
        chem.positive_atoms = int(contents.cell(row, Num_PositiveAtoms).value)
        chem.negative_atoms = int(contents.cell(row, Num_NegativeAtoms).value)
        chem.formal_charge = int(contents.cell(row, FormalCharge).value)
        chem.h_acceptors = int(contents.cell(row, Num_H_Acceptors).value)
        chem.h_donors = int(contents.cell(row, Num_H_Donors).value)
        chem.molecular_solubility = float(contents.cell(row, Molecular_Solubility).value)
        chem.alogp = float(contents.cell(row, ALogP).value)
        chem.logd = float(contents.cell(row, LogD).value)
        chem.molecular_formula = contents.cell(row, Molecular_Formula).value
        chem.smiles = contents.cell(row, Canonical_Smiles).value
        chem.inchl = contents.cell(row, InChI).value
        chem.molecular_savol = float(contents.cell(row, Molecular_SAVol).value)
        chem.save()


def delete_all():
    ChemInfoLocal.objects.all().delete()


def import_data():
    print "delete database"
    delete_all()

    f = xlrd.open_workbook(DATA_FILE)
    contents = f.sheet_by_name(SHEET_NAME)
    print "rows:%s, cols:%s" % (contents.nrows, contents.ncols)
    for i in xrange(contents.nrows):
        try:
            write_row_record(i, contents)
        except Exception, err:
            print (i+2), err


if __name__ == "__main__":
    import_data()
