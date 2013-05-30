import numpy as np
from random import choice, shuffle
from sklearn import ensemble, svm, linear_model
from sklearn.feature_extraction import DictVectorizer

from  common_predict import read_data_col, create_matrix

F = 0.95

COLUMNS = (
    ('TF', '../npapers.train.dat', 4),
    ('venue', '../venue.train.dat', 3),
    ('njournal', '../nvenue.train.dat', 3),
    ('nconference', '../nvenue.train.dat', 4),
    ('name', '../name.train.dat', 3),
    ## ('nameinit', '../name.train.dat', 4),
#    ('nname', '../nname.train.dat', 3),
    ('npapers', '../npapers.train.dat', 3),
    ('nauthors', '../nauthors.train.dat', 3),
#    ('coauthors', '../coauthors_diff.train.dat', 3),
    ## ('zcoauthors', '../coauthors_diff.train.dat', 4),
#    ('affiliation', '../affiliation.train.dat', 3),
    )

if __name__ == '__main__':
    dataCols = dict([(colName, read_data_col(fileName, valCol=valCol))
                     for colName, fileName, valCol in COLUMNS])
    data, colnames = create_matrix(dataCols)
    print colnames
    
    cimt = colnames.index('TF')
    y = data[:, cimt]
    x = data[:, [c for c in range(len(colnames)) if c != cimt]]

    N = len(y)
    ntrain = int(N * F)
    ttindices = range(N)
    shuffle(ttindices)
    yTrain = y[ttindices[:ntrain], :]
    xTrain = x[ttindices[:ntrain], :]
    yTest = y[ttindices[ntrain+1:], :]
    xTest = x[ttindices[ntrain+1:], :]

    print xTrain.shape

    rf = ensemble.RandomForestClassifier(
        n_estimators=100,
        ## criterion='entropy',
        verbose=1,
        n_jobs=-1,
        ## oob_score=True,
        ## min_samples_leaf=1,
        )
    rf.fit(xTrain, yTrain)

    print rf.score(xTrain, yTrain)
    print rf.score(xTest, yTest)
    
    print rf.predict_proba(xTest)
    print rf.predict(xTest)
    print yTest

    print rf.get_params()

    ## # SVM
    ## svc = svm.SVC(kernel='rbf')
    ## svc.fit(xTrain, yTrain)
    ## print svc.score(xTrain, yTrain)
    ## print svc.score(xTest, yTest)

    ## # Logit
    ## logit = linear_model.LogisticRegression()
    ## logit.fit(xTrain, yTrain)
    ## print logit.score(xTrain, yTrain)
    ## print logit.score(xTest, yTest)

