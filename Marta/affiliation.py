import sys
import re
from numpy import mean
from Bio.pairwise2 import align

def affil_align_score(t1, t2):
    maxScore = 0
    alignment = align.globalxx(t1, t2)
##    print alignment 
    for an_al in alignment:
        score = float(an_al[2]) / float(an_al[4])
        if score > maxScore:
            maxScore = score
    return maxScore

def get_affsauthors(aids):
    affil={}
    linestr = ''
    lines = open('/export/home/shared/Projects/kaggle_kdd/Roger/Data/Author.csv').readlines()[1:]
    for line in lines:
        linestr += line.strip()
        try:
            aid = linestr.strip().split(',')[0]
            theaffiliation = linestr.strip().split(',')[2]
            affil[aid] = theaffiliation
            linestr = ''
            ## print >> sys.stderr, paperid, kws[paperid]
        except IndexError:
            pass
    return affil

    
def get_affspapers(aids):

    affil=dict( (aid,{}) for aid in aids)
    linestr = ''
    lines = open('/export/home/shared/Projects/kaggle_kdd/Roger/Data/PaperAuthor.csv').readlines()[1:]
    for line in lines:
        linestr += line.strip()
        try:
            paperid = linestr.strip().split(',')[0]
            aid = linestr.strip().split(',')[1]
            theaffiliation = linestr.strip().split(',')[3]
            linestr = ''
            ## print >> sys.stderr, paperid, kws[paperid]
#            print aid
        except IndexError:
            pass
        try:
            affil[aid][paperid] = theaffiliation
#            print aid,paperid,theaffiliation
        except KeyError:
            pass
    return affil

def get_train():
    lines = open('/export/home/shared/Projects/kaggle_kdd/Roger/Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[aid] = conf.split()
        deleted[aid] = dele.split()
    return confirmed, deleted


if __name__ == '__main__':
    confirmed, deleted = get_train()

    aids=confirmed.keys()
    print 'r1'
    affil_auth = get_affsauthors(aids)
    print 'r2'
    affil_paper = get_affspapers(aids)
    print 'r3'

    


    for aid in confirmed:
        all = confirmed[aid] + deleted[aid]
##        print len (affil_paper[aid]), len(all)
        affila=affil_auth[aid]
        affil_p=affil_paper[aid]
        for pid in confirmed[aid]:
            affilp=affil_p[pid]
            scorea,scorep,scorem=0,0,0
            if affilp!='':
                if affila !='':
                    scorea= affil_align_score(affilp, affila)
                scorep = mean(
                    [affil_align_score(affilp, affil_p[pid2])
                     for pid2 in all if pid2 != pid ]
                    )
                scorem = max(scorea,scorep)    
            print >> sys.stderr, aid, pid, scorea,scorep, scorem,'T'

        for pid in  deleted[aid]:
            affilp=affil_p[pid]
            scorea,scorep,scorem=0,0,0
            if affilp!='':
                if affila !='':
                    scorea= affil_align_score(affilp, affila)
                scorep = mean(
                    [affil_align_score(affilp, affil_p[pid2])
                     for pid2 in all if pid2 != pid ]
                    )
                scorem = max(scorea,scorep)    
            print >> sys.stderr, aid, pid, scorea,scorep, scorem,'F'
