import sys
import re
from numpy import mean
from Bio.pairwise2 import align

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
    kws, linestr = {}, ''
    lines = open('Data/Paper.csv').readlines()[1:]
    for line in lines:
        linestr += line.strip()
        try:
            paperid = linestr.strip().split(',')[0]
            kwstring = linestr.strip().split(',')[5]
            thekws = parse_kw(kwstring)
            if thekws != []:
                kws[paperid] = thekws
            linestr = ''
            ## print >> sys.stderr, paperid, kws[paperid]
        except IndexError:
            pass
    return kws

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
    kws = get_kws()

    print kws['559225']

    for aid in confirmed:
        all = confirmed[aid] + deleted[aid]

        for pid in [p for p in deleted[aid] if kws.has_key(p)]:
            score = mean(
                [kw_align_score(kws[pid], kws[pid2])
                 for pid2 in all
                 if pid2 != pid and kws.has_key(pid2)]
                )
            print aid, pid, score, 'F'

        for pid in [p for p in confirmed[aid] if kws.has_key(p)]:
            score = mean(
                [kw_align_score(kws[pid], kws[pid2])
                 for pid2 in all
                 if pid2 != pid and kws.has_key(pid2)]
                )
            print aid, pid, score, 'T'

