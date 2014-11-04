#coding: utf-8
import os
import glob


def main():
    for path in glob.glob('data/csv/*.csv'):
        i = 0
        name = os.path.basename(path).split('.')[0]
        model_name = name.split('-')[0].lower()

        output = ['#coding:utf-8', 'from numpy import matrix']

        with open(path, 'r') as f:
            for line in f.readlines():
                if i == 0:
                    line = line.replace(',', ' ')
                    line = line.strip('\n').split('\r')[0]
                    output.append("#" + line)
                    output.append("%sX = matrix([" % model_name)
                else:
                    line = line.strip('\n').split('\r')[0]
                    if ',' not in line:
                        continue
                    data = line.split(',')
                    if not data[0]:
                        continue
                    output.append('[%s],' % (','.join(data[1:])))
                i = i + 1

        output.append('])')

        with open('../chemistry/calcore/matrix/%s.py' % model_name, 'wb') as f:
            f.writelines("\n".join(output))
            print 'finish write %s.py' % model_name


if __name__ == "__main__":
    main()
