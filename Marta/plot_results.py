import sys
import os
sys.path.append('/home/marta/Tools/')
sys.path.append('/home/marta/Tools/PyGrace')
sys.path.append('/Users/marta/Tools/PyGrace')
sys.path.append('/Users/marta/Tools/')

from PyGrace.grace import Grace
from numpy import *


def PlotCDF(datat, dataf,title=''):

    grace = Grace()
    graph = grace.add_graph()
    graph.xaxis.label.text = 'Score'
    graph.yaxis.label.text = 'CDF'
    graph.title.text= title

    graph.xaxis.ticklabel.format='decimal'
    graph.xaxis.ticklabel.prec=2
    # graph.xaxis.tick.major = 4
    # graph.xaxis.tick.minor_ticks = 0
    dataset = graph.add_dataset(datat)#), legend=country)
    dataset.symbol.shape = 0
    dataset.line.type = 3
    dataset.line.color=1
    dataset = graph.add_dataset(dataf)#), legend=country)
    dataset.symbol.shape = 0
    dataset.line.type = 3
    dataset.line.color=2

    graph.set_world_to_limits()
    grace.write_file(title+'.agr')

    

def ConstructCDF(data):

    data.sort()
    count=0.
    l=float(len(data))
    d0=data[0]
    cdf=[]
    for d in data:
        count+=1./l
        
        if d>d0:
            cdf.append((d0,count))
            d0=d

    cdf.append((d0,count))
    return cdf

if __name__ == '__main__':

    fname = sys.argv[1]
    results= open(fname).readlines()
    data={'F':[],'T':[]}
    for line in results:
##        print line
        tf=line.strip().split()[-1]
        score=float(line.strip().split()[2])
        data[tf].append(score)


    datat=ConstructCDF(data['T'])   
    dataf=ConstructCDF(data['F'])   
    title=fname[0:-4]

    PlotCDF(datat, dataf,title=title)  

