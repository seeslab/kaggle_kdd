import sys
import numpy as np
from random import choice, shuffle
from sklearn import ensemble, svm, linear_model
from sklearn.feature_extraction import DictVectorizer

from  common_predict import read_data_col, create_matrix
sys.path.append('..')
from common import get_valid

COLUMNS = (
    ('TF', '../npapers', 4),
    ('venue', '../venue', 3),
    ('name', '../name', 3),
    ## ('nameinit', '../name.results.dat', 4),
    ('nname', '../nname', 3),
    ('npapers', '../npapers', 3),
    ('nauthors', '../nauthors', 3),
    ## ('coauthors', '../coauthors_diff', 3),
    ## ('zcoauthors', '../coauthors_diff', 4),
    ## ('affiliation', '../paper_affil', 3),
    )

def train_models(columns, rf=True, svm=False, logit=False):
    # Prepare the data
    dataCols = dict(
        [(colName,
          read_data_col('%s.train.dat' % fileName, valCol=valCol))
         for colName, fileName, valCol in columns]
        )
    data, colnames = create_matrix(dataCols)
    cimt = colnames.index('TF')
    y = data[:, cimt]
    x = data[:, [c for c in range(len(colnames)) if c != cimt]]

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

    return {'models' : models, 'colnames' : colnames}

        
if __name__ == '__main__':
    # Read validation file
    validation = get_valid()

    # Read scores for validation author-paper pairs
    validDataCols = dict(
        [(colName,
          read_data_col('%s.valid.dat' % fileName, valCol=valCol))
         for colName, fileName, valCol in COLUMNS
         if colName != 'TF']
        )

    # Create ordered list of papers for each author in the validation set
    models = {}
    for aid in validation:
        decorated = []
        for pid in validation[aid]:
            # the available columns for this author-paper pair
            cols = [col
                    for col in validDataCols
                    if validDataCols[col][aid].has_key(pid)]
            cols.sort()
            # train the model if necessary (i.e. if this is the first
            # time we see exactly these columns)
            modelName = '_'.join(cols)
            if modelName not in models:
                models[modelName] = train_models(columns)
            # validation columns
            xValid = [validDataCols[col][aid][pid]
                      for col in models[modelName]['colnames']]
            # make the prediction
            decorated.append(
                (models[modelName]['models']['rf'].predict_proba(xValid)[1],
                 pid)
                )
        decorated.sort()
        print aid, decorated
