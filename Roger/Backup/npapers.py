import sys
import gc
from copy import deepcopy
from random import choice
from numpy import log, mean, std
from scipy.misc import factorial
from scipy.sparse import coo_matrix
import scipy.sparse.linalg as sp

from common import get_author_papers, get_train, get_valid


if __name__ == '__main__':
    print >> sys.stderr, 'Reading data...'
    papers, authors = get_author_papers()

    print >> sys.stderr, 'Calculating scores for train set...'
    confirmed, deleted = get_train()
    outf = open('npapers.train.dat', 'w')
    for aid in confirmed:
        allPapers = confirmed[aid] + deleted[aid]
        for p1 in allPapers:
            if p1 in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            print >> outf, aid, p1, len(papers[aid]), tf
    outf.close()

    print >> sys.stderr, 'Calculating scores for validation set...'
    validation = get_valid()
    outf = open('npapers.valid.dat', 'w')
    for aid in validation:
        allPapers = validation[aid]
        for p1 in allPapers:
            print >> outf, aid, p1, len(papers[aid])
    outf.close()
