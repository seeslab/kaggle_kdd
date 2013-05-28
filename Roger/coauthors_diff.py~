import sys
import gc
from copy import deepcopy
from random import choice
from numpy import log, mean, std
from scipy.misc import factorial
from scipy.sparse import coo_matrix
import scipy.sparse.linalg as sp

from common import get_valid, get_author_papers, get_train

# Do a random path in the author-paper bipartite network
def random_path(papers, authors, authorOri, nstep=10):
    current, visited = authorOri, []
    for step in range(nstep):
        # add next step in the sequence
        current = choice(authors[choice(papers[current])])
        visited.append(current)
    return visited

# Get the average distace (=#steps to first visit) between coauthors
# of a target paper
def paper_coauth_distance(target, papers, authors, nstep=10, npath=100):
    coauthors = authors[target]
    ds = []
    for coau1 in coauthors:
        paths = [random_path(papers, authors, coau1, nstep=nstep)
                 for i in range(npath)]
        for coau2 in [c for c in coauthors if c != coau1]:
            ds += [
                path.index(coau2)+1 if coau2 in path else nstep+1
                for path in paths
            ]
    if ds != []:
        return mean(ds)
    else:
        return None
    
def get_paper_score(target, others, papers, authors, nstep=10, npath=100):
    targetScore = paper_coauth_distance(target, papers, authors,
                                        nstep=nstep, npath=npath)
    if targetScore == None:
        return None, None
    else:
        otherScores = [paper_coauth_distance(other, papers, authors,
                                             nstep=nstep, npath=npath)
                       for other in others]
        otherScores = [s for s in otherScores if s != None]
        stddev = std(otherScores)
        if stddev < 1.e-6:
            return None, targetScore
        else:
            return (targetScore - mean(otherScores)) / stddev, targetScore

if __name__ == '__main__':
    try:
        doNAuthors = int(sys.argv[1])
        startAuthorBatch = int(sys.argv[2])
    except:
        doNAuthors, startAuthorBatch = None, None
    

    print >> sys.stderr, 'Reading data...'
    papers, authors = get_author_papers()
    confirmed, deleted = get_train()

    print >> sys.stderr, 'Calculating scores...'
    aids = confirmed.keys()[:]
    naids = len(aids)
    if doNAuthors != None:
        aids = confirmed.keys()[
            min(naids, doNAuthors * (startAuthorBatch - 1)) :
            min(naids, doNAuthors * startAuthorBatch)
            ]

    for aid in aids:
        allPapers = confirmed[aid] + deleted[aid]
        for p1 in allPapers:
            if p1 in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            others = [p for p in allPapers if p != p1]
            zs, s = get_paper_score(p1, others, papers, authors,
                                    nstep=10, npath=25)
            if zs != None and s != None:
                print aid, p1, s, zs, tf
