import sys

from common import get_author_papers, get_train, get_valid

from kaggle_kdd.models import *
from fabric.api import *

@task
def get_nauthors():
    print >> sys.stderr, 'Reading data...'
    papers, authors = get_author_papers()
    confirmed, deleted = get_train()

    print >> sys.stderr, 'Calculating scores for train set...'
    confirmed, deleted = get_train()
    outf = open('nauthors.train.dat', 'w')
    for aid in confirmed:
        allPapers = confirmed[aid] + deleted[aid]
        for p1 in allPapers:
            if p1 in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            print >> outf, aid, p1, len(authors[p1]), tf
    outf.close()

    print >> sys.stderr, 'Calculating scores for validation set...'
    validation = get_valid()
    outf = open('nauthors.valid.dat', 'w')
    for aid in validation:
        allPapers = validation[aid]
        for p1 in allPapers:
            print >> outf, aid, p1, len(authors[p1])
    outf.close()
    

if __name__ == '__main__':
    get_nauthors()
