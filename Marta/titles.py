import sys
import re
from numpy import mean
from Bio.pairwise2 import align

def title_align_score(t1, t2):
    maxScore = 0
    alignment = align.globalxx(t1, t2)
    for an_al in alignment:
        score = float(an_al[2]) / float(an_al[4])
        if score > maxScore:
            maxScore = score
    return maxScore

def get_titles():
    title, linestr = {}, ''
    lines = open('Data/Paper.csv').readlines()[1:]
    for line in lines:
        linestr += line.strip()
        try:
            paperid = linestr.strip().split(',')[0]
            kwstring = linestr.strip().split(',')[5]
            thetitle = linestr.strip().split(',')[1]
            title[paperid] = thetitle
            linestr = ''
            ## print >> sys.stderr, paperid, kws[paperid]
        except IndexError:
            pass
    return title

def get_train():
    lines = open('Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[aid] = conf.split()
        deleted[aid] = dele.split()
    return confirmed, deleted


if __name__ == '__main__':
    confirmed, deleted = get_train()
    title = get_titles()

    quick = {}

    for aid in confirmed:
        all = confirmed[aid] + deleted[aid]

        for pid in [p for p in confirmed[aid] if title.has_key(p)]:
            score = mean(
                [title_align_score(title[pid], title[pid2])
                 for pid2 in all
                 if pid2 != pid and title.has_key(pid2)]
                )
            print >> sys.stderr, aid, pid, score, 'T'

        for pid in [p for p in deleted[aid] if title.has_key(p)]:
            score = mean(
                [title_align_score(title[pid], title[pid2])
                 for pid2 in all
                 if pid2 != pid and title.has_key(pid2)]
                )
            print >> sys.stderr, aid, pid, score, 'F'


