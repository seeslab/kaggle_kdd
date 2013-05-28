import sys
import re
from numpy import mean
from Bio.pairwise2 import align

from common import get_author_papers, get_train, get_valid

def clean_name(n):
    n = n.replace('.', ' ')
    n = n.strip().upper()
    return ' '.join(n.split())

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
    paperName = get_paper_name()

    confirmed, deleted = get_train()
    outf = open('nname.train.dat', 'w')
    for aid in confirmed:
        all = confirmed[aid] + deleted[aid]
        for pid in confirmed[aid]:
            try:
                score = len(clean_name(paperName[aid][pid]))
                print >> outf, aid, pid, score, 'T'
            except KeyError:
                pass
        for pid in deleted[aid]:
            try:
                score = len(clean_name(paperName[aid][pid]))
                print >> outf, aid, pid, score, 'F'
            except KeyError:
                pass
    outf.close()

    validation = get_valid()
    outf = open('nname.valid.dat', 'w')
    for aid in validation:
        all = validation[aid]
        for pid in all:
            try:
                score = len(clean_name(paperName[aid][pid]))
                print >> outf, aid, pid, score
            except KeyError:
                pass
    outf.close()
