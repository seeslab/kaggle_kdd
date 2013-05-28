import sys
import gc
from copy import deepcopy
from random import choice
from numpy import log, mean, std
from scipy.misc import factorial
from scipy.sparse import coo_matrix
import scipy.sparse.linalg as sp


def get_valid():
    lines = open('Data/Valid.csv').readlines()[1:]
    papers = {}
    for line in lines:
        aid, paps = line.strip().split(',')
        papers[aid] = paps.split()
    return papers

def get_author_papers():
    papers, authors = {}, {}
    lines = open('Data/PaperAuthor.csv').readlines()[1:]
    for line in lines:
        try:
            paperid = line.strip().split(',')[0]
            authorid = line.strip().split(',')[1]
            try:
                papers[authorid].append(paperid)
            except KeyError:
                papers[authorid] = [paperid]
            try:
                authors[paperid].append(authorid)
            except KeyError:
                authors[paperid] = [authorid]
        except IndexError:
            pass
    return papers, authors

def get_train():
    lines = open('Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[aid] = conf.split()
        deleted[aid] = dele.split()
    return confirmed, deleted


if __name__ == '__main__':
    pass
