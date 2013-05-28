import sys
import re
from numpy import mean, std
from Bio.pairwise2 import align

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
        # Exclude authors whose papers are BOTH accepted AND deleted
        conf, dele = conf.split(), dele.split()
        addit = True
        for c in conf:
            if c in dele:
                addit = False
                break
        if addit:
            confirmed[aid] = conf
            deleted[aid] = dele
    return confirmed, deleted


if __name__ == '__main__':
    confirmed, deleted = get_train()
    title = get_titles()

    quick = {}

    for aid in confirmed:
        all = confirmed[aid] + deleted[aid]

        for pid in [p for p in confirmed[aid] if title.has_key(p)]:
            l0 = len(title[pid])
            ls = [len(title[pid2])
                 for pid2 in all
                 if pid2 != pid and title.has_key(pid2)]
            if l0 == 0 or mean(ls) == 0 or std(ls) == 0:
                pass
            else:
                score = abs(l0 - mean(ls)) / std(ls)
                print >> sys.stderr, aid, pid, score, 'T'

        for pid in [p for p in deleted[aid] if title.has_key(p)]:
            l0 = len(title[pid])
            ls = [len(title[pid2])
                 for pid2 in all
                 if pid2 != pid and title.has_key(pid2)]
            if l0 == 0 or mean(ls) == 0 or std(ls) == 0:
                pass
            else:
                score = abs(l0 - mean(ls)) / std(ls)
                print >> sys.stderr, aid, pid, score, 'F'


