#coding: utf-8
import os
import glob
from chemistry.models import ChemInfoLocal

base_dir = os.path.dirname(os.path.abspath(__file__))


def find_smile(cas):
    result = ChemInfoLocal.objects.get(cas=cas)
    return result.smiles


def main():
    for path in glob.glob(base_dir + '/data/csv/*.csv'):
        i = 0
        name = os.path.basename(path).split('.')[0]
        model_name = name.split('-')[0].lower()

        output = set()
        not_found = set()

        with open(path, 'r') as f:
            for line in f.readlines():
                if i == 0:
                    i = i + 1
                    continue
                else:
                    line = line.strip('\n').split('\r')[0]
                    if ',' not in line:
                        continue
                    data = line.split(',')
                    if not data[0]:
                        continue
                    cas = data[0].lstrip('0')
                    output.add(cas)
                i = i + 1

        with open(base_dir + '/data/check/%s.csv' % model_name, 'wb') as f:
            for cas in output:
                try:
                    smile = find_smile(cas)
                except:
                    not_found.add(cas)
                    continue
                f.write("%s %s\n" % (cas, smile))
            print 'finish write %s' % model_name
            print " ".join(not_found)


if __name__ == "__main__":
    main()
