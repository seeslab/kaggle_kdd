import sys
import re
from numpy import mean
from Bio.pairwise2 import align

from common import get_author_papers, get_train, get_valid

from kaggle_kdd.models import *
from fabric.api import *

def kw_align_score(kws1, kws2):
    maxScore = 0.0
    for kw1 in [k for k in kws1 if len(k) > 5]:
        for kw2 in [k for k in kws2 if len(k) > 5]:
            alignment = align.globalxx(kw1, kw2)
            for an_al in alignment:
                score = float(an_al[2]) / float(an_al[4])
                if score > maxScore:
                    maxScore = score
    return maxScore

def parse_kw(kwstring):
    kwstring = kwstring.replace('"', '').upper()
    kw = re.split(';|,|:|\|| - ', kwstring)
    return [k.strip() for k in kw
            if not k.startswith('KEY') and
            k.strip() != '']

def get_kws():
    kws = {}
    for paper in Paper.objects.all():
        kws[paper.id] = parse_kw(paper.keywords_string)
    return kws

@task
def get_kw_score(start=None, nauthors=100):
    kws = get_kws()

    print >> sys.stderr, 'Training set...'
    confirmed, deleted = get_train()
    aids = confirmed.keys()[:]
    naids = len(aids)
    if start != None:
        start=int(start)
        nauthors=int(nauthors)
        aids = aids[
            min(naids, nauthors * (start - 1)) :
            min(naids, nauthors * start)
            ]
        outFileName = 'keywords.train_%d-%d.dat' % (
            min(naids, nauthors * (start - 1)),
            min(naids, nauthors * start)
            )
    else:
        outFileName = 'keywords.train.dat'
    count, tot = 0, len(aids)
    outf = open(outFileName, 'w')
    for aid in aids:
        count += 1
        print >> sys.stderr, '%d / %d' % (count, tot)
        all = confirmed[aid] + deleted[aid]
        for pid in all:
            if pid in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            scoren = len(kws[pid])
            scorea = mean(
                [kw_align_score(kws[pid], kws[pid2])
                 for pid2 in all if pid2 != pid]
                )
            print >> outf, aid, pid, scorea, scoren, tf
    outf.close()

    print >> sys.stderr, 'Valid set...'
    validation = get_valid()
    aids = validation.keys()[:]
    naids = len(aids)
    if start != None:
        aids = aids[
            min(naids, nauthors * (start - 1)) :
            min(naids, nauthors * start)
            ]
        outFileName = 'keywords.valid_%d-%d.dat' % (
            min(naids, nauthors * (start - 1)),
            min(naids, nauthors * start)
            )
    else:
        outFileName = 'keywords.valid.dat'
    count, tot = 0, len(aids)
    outf = open(outFileName, 'w')
    for aid in aids:
        all = validation[aid]
        for pid in all:
            scoren = len(kws[pid])
            scorea = mean(
                [kw_align_score(kws[pid], kws[pid2])
                 for pid2 in all if pid2 != pid]
                )
            print >> outf, aid, pid, scorea, scoren
    outf.close()

if __name__ == '__main__':
    get_kw_score()
