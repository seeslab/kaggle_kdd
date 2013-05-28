import sys
import re
from numpy import mean
from Bio.pairwise2 import align

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
    paperName = get_paper_name()

    for aid in confirmed:
        all = confirmed[aid] + deleted[aid]

        for pid in confirmed[aid]:
            try:
                score = len(clean_name(paperName[aid][pid]))
                print aid, pid, score, 'T'
            except KeyError:
                pass
        for pid in deleted[aid]:
            try:
                score = len(clean_name(paperName[aid][pid]))
                print aid, pid, score, 'F'
            except KeyError:
                pass
        
