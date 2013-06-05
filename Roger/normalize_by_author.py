import sys
import numpy as np

def read_score_file(inFileName):
    inFile = open(inFileName, 'r')
    lines = inFile.readlines()
    inFile.close()
    return [line.strip().split() for line in lines]


def get_means(data):
    if data[0][-1] == 'T' or data[0][-1] == 'F':
        ncol = len(data[0]) - 3
    else:
        ncol = len(data[0]) - 2
    means = [{} for c in range(ncol)]
    for row in data:
        aid = row[0]
        for c in range(ncol):
            try:
                means[c][aid].append(float(row[c+2]))
            except KeyError:
                means[c][aid] = [float(row[c+2])]
    for c in range(ncol):
        for aid in means[c]:
            means[c][aid] = np.mean(means[c][aid])
    return means

if __name__ == '__main__':
    inFileName = sys.argv[1]
    var, tv, extension = inFileName.split('.')
    outFileName = '%s_norm.%s.%s' % (var, tv, extension)

    scores = read_score_file(inFileName)
    means = get_means(scores)
    ncol = len(means)

    outf = open(outFileName, 'w')
    for row in scores:
        aid, pid = row[0], row[1]
        print >> outf, aid, pid,
        for c in range(ncol):
            if means[c][aid] > 0:
                print >> outf, float(row[c+2]) / means[c][aid],
            else:
                print >> outf, 0,
        try:
            print >> outf, row[ncol + 2]
        except IndexError:
            print >> outf, ''
    outf.close()
