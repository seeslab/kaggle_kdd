import sys
from time import strftime, localtime
import numpy as np
from random import choice, shuffle
from sklearn import ensemble, svm, linear_model
from sklearn.feature_extraction import DictVectorizer

from  common_predict import read_data_col, create_matrix
sys.path.append('..')
#from common import get_valid

COLUMNS = (
    ('TF', '../npapers', 4),
    ('njournal', '../nvenue', 3),
    ('nconference', '../nvenue', 4),
    ('venue', '../venue', 3),
    ('name', '../name', 3),
    ## ('nameinit', '../name.results.dat', 4),
#    ('nname', '../nname', 3),
    ('npapers', '../npapers', 3),
    ('nauthors', '../nauthors', 3),
#    ('coauthors', '../coauthors_diff', 3),
    ## ('zcoauthors', '../coauthors_diff', 4),
    ## ('affiliation', '../paper_affil', 3),
    )

def get_valid():
    try:
        lines = open('Data/Valid.csv').readlines()[1:]
    except IOError:
        lines = open('../Data/Valid.csv').readlines()[1:]
    papers = {}
    for line in lines:
        aid, paps = line.strip().split(',')
        papers[int(aid)] = [int(p) for p in paps.split()]
    return papers


def train_models(columns, rf=True, svm=False, logit=False):
    # Prepare the data
    dataCols = dict(
        [(colName,
          read_data_col('%s.train.dat' % fileName, valCol=valCol))
         for colName, fileName, valCol in COLUMNS
         if colName in columns or colName == 'TF']
        )
    data, colnames = create_matrix(dataCols)
    cimt = colnames.index('TF')
    y = data[:, cimt]
    x = data[:, [c for c in range(len(colnames)) if c != cimt]]

    print >> sys.stderr, '\n>> Training model with cols:', colnames
    print >> sys.stderr, x

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

    return {'models' : models, 'colnames' : [c for c in colnames if c!='TF']}


#@task
def make_submission():
    # Read validation file
    validation = get_valid()

    # Read scores for validation author-paper pairs
    validDataCols = dict(
        [(colName,
          read_data_col('%s.valid.dat' % fileName, valCol=valCol))
         for colName, fileName, valCol in COLUMNS
         if colName != 'TF']
        )

    # Train the models and prepare the validation sets
    models, xValid, pairsAP = {}, {}, {}
    for aid in validation:
        for pid in validation[aid]:
            # the available columns for this author-paper pair
            try:
                cols = [col
                        for col in validDataCols
                        if validDataCols[col].has_key(aid)
                        and validDataCols[col][aid].has_key(pid)]
            except:
                print aid, pid, aid in validDataCols[col].keys()
                raise ValueError
            cols.sort()
            # train the model if necessary (i.e. if this is the first
            # time we see exactly these columns)
            modelName = '_'.join(cols)
            if modelName not in models:
                models[modelName] = train_models(cols)
                xValid[modelName] = []
                pairsAP[modelName] = []
            # validation columns
            xValid[modelName].append(
                np.array([validDataCols[col][aid][pid]
                          for col in models[modelName]['colnames']])
                )
            pairsAP[modelName].append((aid, pid))
        
    # Make the predictions
    decorated = {}
    for modelName in models:
        print >> sys.stderr, '\n>> Making predictions for cols:', modelName
        # make all predictions for this model
        print >> sys.stderr, np.array(xValid[modelName])
        print >> sys.stderr, np.array(xValid[modelName]).shape
        pred = models[modelName]['models']['rf'].predict_proba(
            np.array(xValid[modelName])
            )
        print >> sys.stderr, pred
        # extract author-paper scores
        for n in range(len(pairsAP[modelName])):
            aid, pid = pairsAP[modelName][n]
            score = pred[n, 0]
            try:
                decorated[aid].append((score, pid))
            except KeyError:
                decorated[aid] = [(score, pid)]

    # Create the file
    outf = open('submit_%s.csv' % strftime("%Y%m%d_%H:%M:%S", localtime()), 'w')
    print >> outf, 'AuthorId,PaperIds'
    for aid in decorated:
        sortedPapers = decorated[aid]
        sortedPapers.sort()
        print >> outf, \
              str(aid) + ',' + ' '.join([str(pid) for s, pid in sortedPapers])
    outf.close()

        
if __name__ == '__main__':
    make_submission()
