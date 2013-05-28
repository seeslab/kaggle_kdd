import sys
import gc
from copy import deepcopy
from random import choice
from numpy import log
from scipy.misc import factorial
from scipy.sparse import coo_matrix
import scipy.sparse.linalg as sp

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


## def random_path(papers, authors, authorOri, nstep=10):
##     current, visited = authorOri, []
##     for step in range(nstep):
##         # add next step in the sequence
##         current = choice(authors[choice(papers[current])])
##         visited.append(current)
##     return visited


## def paths_to_score(paths, authorNames):
##     visits = dict([(author,
##                     dict([(i+1, []) for i in range(len(paths[0]))]))
##                    for author in authorNames])
##     for path in paths:
##         for n1 in range(len(path)):
##             for n2 in range(n1+1, len(path)):
##                 d = n2-n1
##                 visits[authorNames[n1]][d].append(authorNames[n2])

##     score = dict([(author, {}) for author in authorNames])


## def get_diff_scores(papers, authors, nrep=100):
##     # Get all the random paths
##     paths = []
##     for author in authors:
##         for rep in range(nrep):
##             paths.append(random_path(papers, authors, author))
##     return paths_to_score(paths)

def get_score(authors, papers):
    authorIDs = papers.keys()
    paperIDs = authors.keys()

    authorID2n = dict([(authorIDs[nau], nau) for nau in range(len(authorIDs))])
    paperID2n = dict([(paperIDs[nau], nau) for nau in range(len(paperIDs))])

    # author->paper matrix
    print >> sys.stderr, '> author->paper'
    data, row, col = [], [], []
    for nau in range(len(authorIDs)):
        author = authorIDs[nau]
        norm = float(len(papers[author]))
        for paper in papers[author]:
            data.append(1. / norm)
            row.append(nau)
            col.append(paperID2n[paper])
    A = coo_matrix((data, (row, col)), shape=(len(authorIDs), len(paperIDs)))
        
    # paper->author matrix
    print >> sys.stderr, '> paper->author'
    data, row, col = [], [], []
    for npa in range(len(paperIDs)):
        paper = paperIDs[npa]
        norm = float(len(authors[paper]))
        for author in authors[paper]:
            data.append(1. / norm)
            row.append(npa)
            col.append(authorID2n[author])
    B = coo_matrix((data, (row, col)), shape=(len(paperIDs), len(authorIDs)))

    # author->author transition matrix
    print >> sys.stderr, '> author->author'
    C = A.dot(B)
    A, B = None, None
    gc.collect()
    C.tobsr()

    print >> sys.stderr, '> exp(author->author)'
    L = deepcopy(C)
    for i in range(2, 5):
        print >> sys.stderr, '>> %d' % i
        C = C.dot(C)
        print >> sys.stderr, '>> %d.5' % i
        L += C / factorial(i)
        print >> sys.stderr, '>> %d.9' % i
    C = None
    gc.collect()

    return L
    ## return C.todok() # In dok format, elements can be extracted as C[0, 4]

def get_train():
    lines = open('Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[aid] = conf.split()
        deleted[aid] = dele.split()
    return confirmed, deleted


if __name__ == '__main__':
    print >> sys.stderr, 'Reading data...'
    papers, authors = get_author_papers()
    print >> sys.stderr, 'Calculating scores...'
    get_score(authors, papers)
    
    ## venue = get_venue()
    ## confirmed, deleted = get_train()

    ## P1, P2 = get_ps(confirmed, venue)

    ## for aid in confirmed:
    ##     all = confirmed[aid] + deleted[aid]
    ##     for p1 in all:
    ##         if p1 in confirmed[aid]:
    ##             tf = 'T'
    ##         else:
    ##             tf = 'F'
    ##         others = [p for p in all if p != p1]
    ##         s = get_score(p1, others, venue, P1, P2)
    ##         if s > -.5 :
    ##             print aid, p1, s, tf
