import sys
from copy import deepcopy
from numpy import log

from common import get_author_papers, get_train, get_valid

def get_venue():
    journal, conference, linestr = [], [], ''
    lines = open('Data/Paper.csv').readlines()[1:]
    for line in lines:
        linestr += line.strip()
        print >> sys.stderr, line.strip()
        try:
            sline = linestr.strip().split(',')
            paperid = sline[0]
            kwstring = sline[5]
            title = sline[1]
            confid= int(sline[3])
            jourid= int(sline[4])
            journal.append((paperid, jourid))
            conference.append((paperid, confid))
        except IndexError:
            pass
        except ValueError:
            linestr = ''
            pass
    return dict(journal), dict(conference)

if __name__ == '__main__':
    print >> sys.stderr, 'Reading venue info...'
    journal, conference = get_venue()
    print >> sys.stderr, 'Reading author-paper info...'
    papers, authors = get_author_papers()

    print >> sys.stderr, 'Reading training set...'
    confirmed, deleted = get_train()

    outf = open('nvenue.train.dat', 'w')
    for aid in confirmed:
        all = papers[aid]
        for p1 in [p for p in confirmed[aid] + deleted[aid]]:
            if p1 in confirmed[aid]:
                tf = 'T'
            elif p1 in deleted[aid]:
                tf = 'F'
            else:
                raise WhatTheFuck
            sj = sum([1 for p in all if journal[p] == journal[p1]])
            sc = sum([1 for p in all if conference[p] == conference[p1]])
            print >> outf, aid, p1, sj, sc, tf
    outf.close()

    validation = get_valid()
    outf = open('nvenue.valid.dat', 'w')
    for aid in validation:
        all = papers[aid]
        for p1 in [p for p in all if p in validation[aid]]:
            sj = sum([1 for p in all if journal[p] == journal[p1]])
            sc = sum([1 for p in all if conference[p] == conference[p1]])
            print >> outf, aid, p1, sj, sc
    outf.close()
