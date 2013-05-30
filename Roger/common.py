import sys
import gc
from copy import deepcopy
from random import choice
from numpy import log, mean, std
from scipy.misc import factorial
from scipy.sparse import coo_matrix
import scipy.sparse.linalg as sp

from kaggle_kdd.models import *

def get_valid():
    try:
        lines = open('Data/Valid.csv').readlines()[1:]
    except IOError:
        lines = open('../Data/Valid.csv').readlines()[1:]
    papers = {}
    for line in lines:
        aid, paps = line.strip().split(',')
        papers[int(aid)] = [int(p) for p in paps.split()]
    return papers

def get_train():
    lines = open('Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[int(aid)] = [int(p) for p in conf.split()]
        deleted[int(aid)] = [int(p) for p in dele.split()]
    return confirmed, deleted

# def get_author_papers():
#     papers, authors = {}, {}
#     try:
#         lines = open('Data/PaperAuthor.csv').readlines()[1:]
#     except IOError:
#         lines = open('../Data/PaperAuthor.csv').readlines()[1:]
#     for line in lines:
#         try:
#             paperid = line.strip().split(',')[0]
#             authorid = line.strip().split(',')[1]
#             try:
#                 papers[authorid].append(paperid)
#             except KeyError:
#                 papers[authorid] = [paperid]
#             try:
#                 authors[paperid].append(authorid)
#             except KeyError:
#                 authors[paperid] = [authorid]
#         except IndexError:
#             pass
#     return papers, authors


def get_author_papers():
    papers, authors = {}, {}
    for paper_author in PaperAuthor.objects.all():
        try:
            papers[paper_author.authorId].append(paper_author.paperId)
        except KeyError:
            papers[paper_author.authorId] = [paper_author.paperId]
        try:
            authors[paper_author.paperId].append(paper_author.authorId)
        except KeyError:
            authors[paper_author.paperId] = [paper_author.authorId]

    return papers, authors



if __name__ == '__main__':
    pass
