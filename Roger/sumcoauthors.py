import sys

from common import get_author_papers, get_train, get_valid

from kaggle_kdd.models import *
from fabric.api import *


@task
def get_sum_coauthors():
    print >> sys.stderr, 'Reading data...'
    papers, authors = get_author_papers()

    #Create the number of collaborations between 2 authors
    num_collaborations = {}
    for author in authors.values():
        for i in range(0,len(author)):
            for j in range(i+1,len(author)):
                #Always use the lowest author id as the first key
                if author[i]<author[j]:
                    try:
                        num_collaborations[(author[i], author[j])] += 1
                    except KeyError:
                        num_collaborations[(author[i], author[j])] = 1
                else:
                    try:
                        num_collaborations[(author[j], author[i])] += 1
                    except KeyError:
                        num_collaborations[(author[j], author[i])] = 1


    print >> sys.stderr, 'Calculating scores for train set...'
    confirmed, deleted = get_train()
    print confirmed
    outf = open('npapers.train.dat', 'w')
    for aid in confirmed:
        allPapers = confirmed[aid] + deleted[aid]
        for p1 in allPapers:
            sum_coauthors = 0
            for author in authors[p1]:
                if author<aid:
                    sum_coauthors += num_collaborations[(author,aid)]
                elif aid<author:
                    sum_coauthors += num_collaborations[(aid,author)]

            if p1 in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            print >> outf, aid, p1, sum_coauthors, tf
    outf.close()

    print >> sys.stderr, 'Calculating scores for validation set...'
    validation = get_valid()
    outf = open('npapers.valid.dat', 'w')
    for aid in validation:
        allPapers = validation[aid]
        for p1 in allPapers:
            sum_coauthors = 0
            for author in authors[p1]:
                if author<aid:
                    sum_coauthors += num_collaborations[(author,aid)]
                elif aid<author:
                    sum_coauthors += num_collaborations[(aid,author)]

            if p1 in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            print >> outf, aid, p1, sum_coauthors
    outf.close()

if __name__ == '__main__':
    get_sum_coauthors()
