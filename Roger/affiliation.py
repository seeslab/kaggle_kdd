import sys
import re
from numpy import mean
from Bio.pairwise2 import align

from common import get_author_papers, get_train, get_valid

from kaggle_kdd.models import *
from fabric.api import *

def affil_align_score(t1, t2):
    if t1 == '' or t2 == '':
        return 0
    maxScore = 0
    alignment = align.globalxx(t1, t2)
    for an_al in alignment:
        score = float(an_al[2]) / float(an_al[4])
        if score > maxScore:
            maxScore = score
    return maxScore

def get_affsauthors():
    affil = {}
    for author in Author.objects.all():
        affil[author.id] = author.affiliation
    return affil

    
def get_affspapers():
    affil = {}
    for pa in PaperAuthor.objects.all():
        try:
            affil[pa.authorId][pa.paperId] = pa.affiliation
        except KeyError:
            affil[pa.authorId] = {pa.paperId : pa.affiliation}
    return affil

@task
def get_affiliation_score():
    print >> sys.stderr, 'Loading author reference affiliations...'
    affil_auth = get_affsauthors()
    print >> sys.stderr, 'Loading author-paper table...'
    affil_paper = get_affspapers()

    print >> sys.stderr, 'Creating training...'
    confirmed, deleted = get_train()
    outf = open('affiliation.train.dat', 'w')
    count, tot = 0, len(confirmed)
    for aid in confirmed:
        count += 1
        print >> sys.stderr, '%d / %d' % (count, tot)
        all = confirmed[aid] + deleted[aid]
        for pid in confirmed[aid] + deleted[aid]:
            if pid in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'

            scorea= affil_align_score(affil_paper[aid][pid],
                                      affil_auth[aid])
            ## scorep = mean(
            ##     [affil_align_score(affil_paper[aid][pid],
            ##                        affil_paper[aid][pid2])
            ##      for pid2 in all if pid2 != pid]
            ##     )
            ## scorem = max(scorea,scorep)    
            ## print >> outf, aid, pid, scorea, scorep, scorem, tf
            print >> outf, aid, pid, scorea, tf
    outf.close()

    print >> sys.stderr, 'Creating validation...'
    validation = get_valid()
    outf = open('affiliation.valid.dat', 'w')
    for aid in validation:
        for pid in validation[aid]:
            scorea= affil_align_score(affil_paper[aid][pid],
                                      affil_auth[aid])
            ## scorep = mean(
            ##     [affil_align_score(affil_paper[aid][pid],
            ##                        affil_paper[aid][pid2])
            ##      for pid2 in validation[aid] if pid2 != pid]
            ##     )
            ## scorem = max(scorea,scorep)
            print >> outf, aid, pid, scorea
    outf.close()    


if __name__ == '__main__':
    get_affiliation_score()
