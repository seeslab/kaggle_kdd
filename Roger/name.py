import sys
import re
from numpy import mean
from Bio.pairwise2 import align

from common import get_author_papers, get_train, get_valid

from kaggle_kdd.models import *
from fabric.api import *

def clean_name(n):
    n = n.replace('.', ' ')
    n = n.strip().upper()
    return ' '.join(n.split())

def initialize_name(n):
    n = clean_name(n)
    return ' '.join([s[0] for s in n.split()][:-1] + [n.split()[-1]])

def name_align_score(n1, n2):
    if n1 == '' and n2 == '':
        return -3, -3
    elif n1 == '':
        return -1, -1
    elif n2 == '':
        return -2, -2

    # Full name
    maxScoreFull = 0
    alignment = align.globalxx(clean_name(n1), clean_name(n2))
    for an_al in alignment:
        score = float(an_al[2]) / float(an_al[4])
        if score > maxScoreFull:
            maxScoreFull = score
    ## print clean_name(n1), clean_name(n2), maxScoreFull

    # Initialized name
    maxScoreIni = 0
    alignment = align.globalxx(initialize_name(n1), initialize_name(n2))
    for an_al in alignment:
        score = float(an_al[2]) / float(an_al[4])
        if score > maxScoreIni:
            maxScoreIni = score

    # Done
    return maxScoreFull, maxScoreIni


def get_base_name():
    name = {}
    for author in Author.objects.all():
        name[author.id] = author.name
    return name

def get_paper_name():
    name = {}
    for pa in PaperAuthor.objects.all():
        try:
            name[pa.authorId][pa.paperId] = pa.name
        except KeyError:
            name[pa.authorId] = {pa.paperId : pa.name}
    return name

@task
def get_name_score():
    print >> sys.stderr, 'Loading author-paper table...'
    paperName = get_paper_name()
    print >> sys.stderr, 'Loading author reference names...'
    baseName = get_base_name()

    confirmed, deleted = get_train()
    outf = open('name.train.dat', 'w')
    for aid in confirmed:
        all = confirmed[aid] + deleted[aid]
        for pid in confirmed[aid]:
            try:
                sFull, sInit = name_align_score(paperName[aid][pid],
                                                baseName[aid])
                print >> outf, aid, pid, sFull, sInit, 'T'
            except KeyError:
                pass
        for pid in deleted[aid]:
            try:
                sFull, sInit = name_align_score(paperName[aid][pid],
                                                baseName[aid])
                print >> outf, aid, pid, sFull, sInit, 'F'
            except KeyError:
                pass
    outf.close()
        
    validation = get_valid()
    outf = open('name.valid.dat', 'w')
    for aid in validation:
        all = validation[aid]
        for pid in all:
            try:
                sFull, sInit = name_align_score(paperName[aid][pid],
                                                baseName[aid])
                print >> outf, aid, pid, sFull, sInit
            except KeyError:
                pass
    outf.close()


if __name__ == '__main__':
    get_name_score()
