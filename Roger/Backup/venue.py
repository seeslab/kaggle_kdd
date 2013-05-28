import sys
from copy import deepcopy
from numpy import log

def get_author_papers():
    papers = {}
    lines = open('Data/PaperAuthor.csv').readlines()[1:]
    for line in lines:
        try:
            paperid = line.strip().split(',')[0]
            authorid = line.strip().split(',')[1]
            try:
                papers[authorid].append(paperid)
            except KeyError:
                papers[authorid] = [paperid]
        except IndexError:
            pass
    return papers

def get_venue():
    venue, linestr = {}, ''
    lines = open('Data/Paper.csv').readlines()[1:]
    for line in lines:
        linestr += line.strip()
        try:
            paperid = linestr.strip().split(',')[0]
            kwstring = linestr.strip().split(',')[5]
            title = linestr.strip().split(',')[1]
            confid= int(linestr.strip().split(',')[3])
            jourid= int(linestr.strip().split(',')[4])
            """            if confid > 0 and jourid > 0:
                raise
            elif confid > 0:
                venue[paperid] = 'C%d' % confid
            elif jourid > 0:
                venue[paperid] = 'J%d' % jourid
            else:
                venue[paperid] = '-'
                """
            if jourid > 0 or confid > 0:
                if jourid > confid:
                    venue[paperid] = 'J%d' % jourid
                else:
                    venue[paperid] = 'C%d' % confid
            linestr = ''
        except IndexError:
            pass
        except ValueError:
            linestr = ''
            pass
    return venue
    
def get_train():
    lines = open('Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[aid] = conf.split()
        deleted[aid] = dele.split()
    return confirmed, deleted

def get_ps(confirmed, venue):
    # n1(v1) and n2(v1, v2), and their normalizations
    n1, n2, norm1, norm2 = {}, {}, 0, 0
    for aid, papers in confirmed.items():
        for p1 in [p for p in papers if p in venue]:
            v1 = venue[p1]
            if v1 not in n2:
                n2[v1] = {}
            for p2 in [p for p in confirmed[aid] if p != p1 and p in venue]:
                v2 = venue[p2]
                try:
                    n2[v1][v2] += 1
                except KeyError:
                    n2[v1][v2] = 1
                norm2 += 1
                try:
                    n1[v2] += 1
                except KeyError:
                    n1[v2] = 1
                norm1 += 1

    # normalize
    for p1 in n1:
        n1[p1] /= float(norm1)
    for p1 in n2:
        for p2 in n2[p1]:
            n2[p1][p2] /= float(norm2)

    # done
    return n1, n2, norm1, norm2

def get_score(target, others, venue, P1, P2):
    score, norm = 0, 0
    for other in others:
        try:
            score += P2[venue[target]][venue[other]] / P1[venue[other]]
            if P2[venue[target]][venue[other]] / P1[venue[other]] > 1:
                print >> sys.stderr, venue[target], venue[other], P2[venue[target]][venue[other]], P1[venue[other]]
                raise ValueError
            norm += 1
        except:
            norm += 1
    if norm > 0:
        return score / float(norm)
    else:
        return -1

def ps_without_author(aid, confirmed, venue, P1All, P2All, norm1All, norm2All):
    P1 = deepcopy(P1All)
    P2 = deepcopy(P2All)
    papers = confirmed[aid]
    n1, n2, norm1, norm2 = {}, {}, 0, 0 
    for p1 in [p for p in papers if p in venue]:
        v1 = venue[p1]
        if v1 not in n2:
            n2[v1] = {}
            for p2 in [p for p in confirmed[aid] if p != p1 and p in venue]:
                v2 = venue[p2]
                try:
                    n2[v1][v2] += 1
                except KeyError:
                    n2[v1][v2] = 1
                norm2 += 1
                try:
                    n1[v2] += 1
                except KeyError:
                    n1[v2] = 1
                norm1 += 1

    for v1 in n1:
        P1[v1] = (P1All[v1] * norm1All - n1[v1]) / \
            (norm1All - norm1)
    for v1 in n2:
        for v2 in n2[v1]:
            P2[v1][v2] = (P2All[v1][v2] * norm2All - n2[v1][v2]) / \
                (norm2All - norm2)
    return P1, P2

if __name__ == '__main__':
    venue = get_venue()
    confirmed, deleted = get_train()

    P1All, P2All, norm1All, norm2All = get_ps(confirmed, venue)

    count, tot = 0, len(confirmed)
    for aid in confirmed:
        count += 1
        print >> sys.stderr, '%d / %d' % (count, tot)

        P1, P2 = ps_without_author(
            aid, confirmed, venue, P1All, P2All, norm1All, norm2All
            )
        all = confirmed[aid] + deleted[aid]

        aidConfirmed = confirmed[aid]
        confirmed[aid] = []
        confirmed[aid] = aidConfirmed

        for p1 in all:
            if p1 in confirmed[aid]:
                tf = 'T'
            else:
                tf = 'F'
            others = [p for p in all if p != p1]
            s = get_score(p1, others, venue, P1, P2)
            if s > -.5 :
                print aid, p1, s, tf
