import sys

def get_train():
    lines = open('Data/Train.csv').readlines()[1:]
    confirmed, deleted = {}, {}
    for line in lines:
        aid, conf, dele = line.strip().split(',')
        confirmed[int(aid)] = [int(p) for p in conf.split()]
        deleted[int(aid)] = [int(p) for p in dele.split()]
    return confirmed, deleted

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

if __name__ == '__main__':
    confirmed, deleted = get_train()
    validation = get_valid()

    ## print >> sys.stderr, 'Finding papers in validation set...'
    ## validationPapers = []
    ## for aid, papers in validation.items():
    ##     for paper in papers:
    ##         if paper not in validationPapers:
    ##             validationPapers.append(paper)

    ## print >> sys.stderr, 'Checking in training set...'
    ## for aid in confirmed:
    ##     for paper in confirmed[aid] + deleted[aid]:
    ##         if paper in validationPapers:
    ##             print paper

    print >> sys.stderr, 'Checking in training set...'
    nconfdele = {}
    for aid in confirmed:
        for pid in confirmed[aid]:
            try:
                nconfdele[pid][0] += 1
            except:
                nconfdele[pid] = [1, 0]
        for pid in deleted[aid]:
            try:
                nconfdele[pid][1] += 1
            except:
                nconfdele[pid] = [0, 1]

    for pid in nconfdele:
        norm = sum(nconfdele[pid])
        if norm == 3:
            print float(nconfdele[pid][0]) / float(norm)
