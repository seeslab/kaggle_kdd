import sys
from copy import deepcopy
from numpy import log

from common import get_author_papers, get_train, get_valid

from kaggle_kdd.models import *
from fabric.api import *

def get_venue():
    journal, conference = {}, {}
    for paper in Paper.objects.filter(journal__isnull=False).values('id','journal'):
        journal[ paper['id'] ] = paper['journal']
    for paper in Paper.objects.filter(conference__isnull=False).values('id','conference'):
        conference[ paper['id'] ] = paper['conference']

    return journal, conference

def build_author_venue_count(papers, venue):
    aid2venue = {}
    for aid in papers:
        aid2venue[aid] = {}
        for p in papers[aid]:
            try:
                thevenue = venue[p]
            except KeyError:
                thevenue = -1
            try:
                aid2venue[aid][thevenue] += 1
            except KeyError:
                aid2venue[aid][thevenue] = 1
    return aid2venue

@task
def get_nvenue():
    print >> sys.stderr, 'Reading venue info...'
    journal, conference = get_venue()
    print >> sys.stderr, 'Reading author-paper info...'
    papers, authors = get_author_papers()

    print >> sys.stderr, 'Counting papers in journals...'
    aid2journal = build_author_venue_count(papers, journal)
    print >> sys.stderr, 'Counting papers in conferences...'
    aid2conference = build_author_venue_count(papers, conference)

    print >> sys.stderr, 'Training set...'
    confirmed, deleted = get_train()
    outf = open('nvenue.train.dat', 'w')
    for aid in confirmed:
        for p1 in [p for p in confirmed[aid] + deleted[aid]]:
            if p1 in confirmed[aid]:
                tf = 'T'
            elif p1 in deleted[aid]:
                tf = 'F'
            else:
                raise WhatTheFuck
            try:
                sj = aid2journal[aid][journal[p1]]
            except KeyError:
                sj = aid2journal[aid][-1]                
            try:
                sc = aid2conference[aid][conference[p1]]
            except KeyError:
                sc = aid2conference[aid][-1]
            print >> outf, aid, p1, sj, sc, tf
    outf.close()

    print >> sys.stderr, 'Validation set...'
    validation = get_valid()
    outf = open('nvenue.valid.dat', 'w')
    for aid in validation:
        for p1 in validation[aid]:
            try:
                sj = aid2journal[aid][journal[p1]]
            except KeyError:
                sj = aid2journal[aid][-1]                
            try:
                sc = aid2conference[aid][conference[p1]]
            except KeyError:
                sc = aid2conference[aid][-1]
            print >> outf, aid, p1, sj, sc
    outf.close()

if __name__ == '__main__':
    get_nvenue()
