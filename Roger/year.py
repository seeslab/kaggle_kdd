import sys
import re
from numpy import mean, std, isnan
from Bio.pairwise2 import align

from common import get_author_papers, get_train, get_valid

from kaggle_kdd.models import *
from fabric.api import *

def get_year():
    year = {}
    for p in Paper.objects.all():
        year[p.id] = p.year
    return year

@task
def get_year_score():
    print >> sys.stderr, 'Loading publication years...'
    year = get_year()

    print >> sys.stderr, 'Creating training...'
    confirmed, deleted = get_train()
    outf = open('year.train.dat', 'w')
    count, tot = 0, len(confirmed)
    for aid in confirmed:
        count += 1
        print >> sys.stderr, '%d / %d' % (count, tot)
        all = confirmed[aid] + deleted[aid]
        paperYears = [year[p] for p in all]
        for pid in all:
            if pid in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            score = (year[pid] - mean(paperYears)) / std(paperYears)
            if isnan(score):
                score = -100
            print >> outf, aid, pid, score, tf
    outf.close()

    print >> sys.stderr, 'Creating validation...'
    validation = get_valid()
    outf = open('year.valid.dat', 'w')
    for aid in validation:
        all = validation[aid]
        paperYears = [year[p] for p in all]
        for pid in all:
            score = (year[pid] - mean(paperYears)) / std(paperYears)
            if isnan(score):
                score = -100
            print >> outf, aid, pid, score
    outf.close()    


if __name__ == '__main__':
    get_year_score()
