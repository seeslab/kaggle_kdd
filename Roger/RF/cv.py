import sys
from time import strftime, localtime
import numpy as np
from random import choice, shuffle, seed
from sklearn import ensemble, svm, linear_model
from sklearn.feature_extraction import DictVectorizer

from  common_predict import read_data_col, create_matrix
sys.path.append('..')

#seed(1111)

F = 0.95
NREP = 20

COLUMNS = (
    ('TF', '../npapers', 4),
    ('njournal', '../nvenue', 3),
    ('nconference', '../nvenue', 4),
    ('npapers', '../npapers', 3),
    ('nauthors', '../nauthors', 3),
    ('sumcoauthors', '../sumcoauthors', 3),
    ('venue', '../venue', 3),
    ('name', '../name', 3),
    ## ('nameinit', '../name', 4),
#    ('nname', '../nname', 3),
#    ('coauthors', '../coauthors_diff', 3),
    ## ('zcoauthors', '../coauthors_diff', 4),
    ('affiliation', '../affiliation', 3),
    ('year', '../year', 3),
    ('nvalidated', '../nvalidated', 3),
    ('kw', '../keywords', 3),
    ('nkw', '../keywords', 4),
    ('kwNorm', '../keywords_norm', 3),
    )

def get_train():
    lines = open('../Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[int(aid)] = [int(p) for p in conf.split()]
        deleted[int(aid)] = [int(p) for p in dele.split()]
    return confirmed, deleted


def train_models(x, y, rf=True, svm=False, logit=False):
    # Fit the models
    models = {}
    if rf:
        rfModel = ensemble.RandomForestClassifier(
            n_estimators=100,
            ## criterion='entropy',
            verbose=1,
            n_jobs=-1,
            ## oob_score=True,
            ## min_samples_leaf=1,
            )
        rfModel.fit(x, y)
        models['rf'] = rfModel

    if svm:
        svmModel = svm.SVC(kernel='rbf')
        svmModel.fit(x, y)
        models['svm'] = svmModel

    if logit:
        logitModel = linear_model.LogisticRegression()
        logitModel.fit(x, y)
        models['logit'] = logitModel

    return models


# -----------------------------------------------------------------------------
#
def cross_validation(logit=False):
    # Split authors in train/validation
    confirmed, deleted = get_train()
    aids = confirmed.keys()
    shuffle(aids)
    cutPoint = int(len(aids) * F)
    aidsTrain = aids[:cutPoint]
    aidsValid = aids[cutPoint:]

    # Prepare the training data
    dataCols = dict(
        [(colName,
          read_data_col('%s.train.dat' % fileName, valCol=valCol))
         for colName, fileName, valCol in COLUMNS]
        )
    data, colnames = create_matrix(dataCols, exclude_aids=aidsValid)
    cimt = colnames.index('TF')
    ytrain = data[:, cimt]
    xtrain = data[:, [c for c in range(len(colnames)) if c != cimt]]
    # validation
    data, colnames2, pairs = create_matrix(dataCols,
                                           exclude_aids=aidsTrain,
                                           return_pairs=True)
    if colnames2 != colnames:
        raise WTF
    yvalid = data[:, cimt]
    xvalid = data[:, [c for c in range(len(colnames)) if c != cimt]]

    print >> sys.stderr, '==> %s train; %s valid <==' % (str(xtrain.shape),
                                                         str(xvalid.shape))

    # Train the model
    models = train_models(xtrain, ytrain, logit=logit)

    # Calculate performance of each algorithm
    performance = {}
    for algorithm in models:
        print >> sys.stderr, '\n\n--> %s <--\n' % algorithm
        print >> sys.stderr, models[algorithm]

        # make the predictions
        predBin = models[algorithm].predict(xvalid)
        pred = models[algorithm].predict_proba(xvalid)
        print >> sys.stderr, ''
        print >> sys.stderr, yvalid
        print >> sys.stderr, predBin
        print >> sys.stderr, pred

        # extract author-paper scores
        decorated = {}
        for n in range(len(pairs)):
            aid, pid = pairs[n]
            score = pred[n, 0]
            try:
                decorated[aid].append((score, pid, yvalid[n]))
            except KeyError:
                decorated[aid] = [(score, pid, yvalid[n])]

        # get the MAP
        MAPs = []
        for aid in decorated:
            sortedPapers = decorated[aid]
            sortedPapers.sort()
            ntrue, ntot, MAPTerms = 0, 0, []
            for s, p, tf in sortedPapers:
                ntot += 1
                if tf == 1:
                    ntrue += 1
                    MAPTerms.append(float(ntrue)/float(ntot))
            MAPs.append(np.mean(MAPTerms))

        # output results
        performance[algorithm] = np.mean(MAPs)
        print >> sys.stderr, '\n>> %s: %f' % (algorithm, np.mean(MAPs))

    # Done
    print >> sys.stderr, '\n'
    return performance
        
if __name__ == '__main__':
    performance = {}
    for rep in range(NREP):
        thisPerf = cross_validation(logit=True)
        for algorithm in thisPerf:
            try:
                performance[algorithm].append(thisPerf[algorithm])
            except KeyError:
                performance[algorithm] = [thisPerf[algorithm]]

    print >> sys.stderr, '\n\n==> AVERAGE PERFORMANCE <==\n'
    for algorithm in thisPerf:
        print >> sys.stderr, algorithm, \
              np.mean(performance[algorithm]), \
              np.std(performance[algorithm]) / np.sqrt(NREP), \
              np.std(performance[algorithm])
    print >> sys.stderr, ''
