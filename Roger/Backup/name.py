import sys
import re
from numpy import mean
from Bio.pairwise2 import align

from common import get_author_papers, get_train, get_valid

def clean_name(n):
    n = n.replace('.', ' ')
    n = n.strip().upper()
    return ' '.join(n.split())

def initialize_name(n):
    n = clean_name(n)
    return ' '.join([s[0] for s in n.split()][:-1] + [n.split()[-1]])

def name_align_score(n1, n2):
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
    name, linestr = {}, ''
    lines = open('Data/Author.csv').readlines()[1:]
    for line in lines:
        linestr += line.strip()
        try:
            authorid = linestr.strip().split(',')[0]
            thename = linestr.strip().split(',')[1]
            name[authorid] = thename
            linestr = ''
            ## print >> sys.stderr, paperid, kws[paperid]
        except IndexError:
            pass
    return name

def get_paper_name():
    name, linestr = {}, ''
    lines = open('Data/PaperAuthor.csv').readlines()[1:5000000]
    for line in lines:
        try:
            paperid = line.strip().split(',')[0]
            authorid = line.strip().split(',')[1]
            thename = line.strip().split(',')[2]
            if authorid not in name:
                name[authorid] = {}
            name[authorid][paperid] = thename
        except IndexError:
            pass
    return name

if __name__ == '__main__':
    baseName = get_base_name()
    paperName = get_paper_name()

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
