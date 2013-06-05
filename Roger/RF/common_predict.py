import numpy as np
from random import choice, shuffle
from sklearn import ensemble, svm, linear_model
from sklearn.feature_extraction import DictVectorizer

def read_data_col(inFileName, aidCol=1, pidCol=2, valCol=3):
    inFile = open(inFileName,'r')
    lines = inFile.readlines()
    inFile.close()
    data = {}
    for line in lines:
        sline = line.strip().split()
        aid = int(sline[aidCol-1])
        pid = int(sline[pidCol-1])
        try:
            val = float(sline[valCol-1]) 
        except ValueError:
            val = int(sline[valCol-1] == 'T')
        try:
            data[aid][pid] = val
        except KeyError:
            data[aid] = {pid : val}
    return data


def create_matrix(dataCols, exclude_aids=[], return_pairs=False):
    # Find aid-pid pairs
    pairs = []
    for aid in [a for a in dataCols.values()[0] if a not in exclude_aids]:
        for pid in dataCols.values()[0][aid]:
            addpair = True
            for dataCol in dataCols.values():
                try:
                    tmp = dataCol[aid][pid]
                except KeyError:
                    addpair = False
            if addpair:
                pairs.append((aid, pid))

    # Create the list of dictionaries
    dataDict = [{} for i in pairs]
    for n in range(len(pairs)):
        aid, pid = pairs[n]
        for dataName, data in dataCols.items():
            dataDict[n][dataName] = data[aid][pid]

    # Create the matrix
    vec = DictVectorizer()
    data = vec.fit_transform(dataDict).toarray()
    colnames = vec.get_feature_names()

    # Done
    if return_pairs:
        return data, colnames, pairs
    else:
        return data, colnames


