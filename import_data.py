__author__ = 'jduch'


from fabric.api import *
import csv
from kaggle_kdd.models import *

@task
def import_data():
    # with open('data/Author.csv','rt') as csv_file:
    #     count = -1
    #     for row in csv.reader(csv_file, delimiter=','):
    #         count += 1
    #         if count == 0: continue
    #         author, is_new = Author.objects.get_or_create(id = int(row[0]),
    #                                                       name = row[1],
    #                                                       affiliation = row[2])
    #         if is_new:
    #             print count, "Author",row[1],"added."
    #
    # with open('data/Journal.csv','rt') as csv_file:
    #     count = -1
    #     for row in csv.reader(csv_file, delimiter=','):
    #         count += 1
    #         if count == 0: continue
    #         journal, is_new = Journal.objects.get_or_create(id = int(row[0]),
    #                                                         shortname = row[1],
    #                                                         fullname = row[2],
    #                                                         homepage = row[3])
    #         if is_new:
    #             print count, "Journal",row[1],"added."
    #
    # with open('data/Conference.csv','rt') as csv_file:
    #     count = -1
    #     for row in csv.reader(csv_file, delimiter=','):
    #         count += 1
    #         if count == 0: continue
    #         conference, is_new = Conference.objects.get_or_create(id = int(row[0]),
    #                                                               shortname = row[1],
    #                                                               fullname = row[2],
    #                                                               homepage = row[3])
    #         if is_new:
    #             print count, "Conference",row[1],"added."


    # count = -1
    # for row in csv.reader(open('data/PaperShort.csv','r')):
    #     count += 1
    #     if count == 0: continue
    #
    #     paper, is_new = Paper.objects.get_or_create(id = int(row[0]))
    #
    #     print count, "Paper",row[0],"added."
    #
    #     paper.title = unicode(row[1], 'utf-8')
    #     paper.year = int(row[2])
    #     paper.keywords_string = unicode(row[5], 'utf-8')
    #
    #     if int(row[3]) == 0 or int(row[3]) == -1:
    #         paper.conference = None
    #     else:
    #         try:
    #             paper.conference = Conference.objects.get(id=int(row[3]))
    #         except:
    #             paper.conference = None
    #
    #     if int(row[4]) == 0 or int(row[4]) == -1:
    #         paper.journal = None
    #     else:
    #         try:
    #             paper.journal = Journal.objects.get(id=int(row[4]))
    #         except:
    #             paper.conference = None
    #
    #     paper.save()

    for i in range(14,26):
        print "*"*50
        print "*"*50
        print "*"*50
        print 'data/PaperAuthor_%02d.csv'%i
        filein = open('data/PaperAuthor_%02d.csv'%i,'r')
        count = -1
        for row in csv.reader(filein):
            count += 1
            if count == 0: continue

            #author = Author.objects.get(id=int(row[1]))
            #paper = Paper.objects.get(id=int(row[0]))

            pa = PaperAuthor.objects.create(paperId = int(row[0]),
                                            authorId = int(row[1]),
                                            name = row[2],
                                            affiliation = row[3])

            if count % 1000 == 0:
                print count, "PaperAuthor",row[0],"-",row[1],"added."

@task
def countAuthors():
    for author in Author.objects.all()[:10]:
        print author.name

@task
def break_file():

    filein=open('data/PaperAuthor.csv','r')
    numfile=0
    count=0
    fileout=open('data/PaperAuthor_%02d.csv'%numfile,'w')
    print >>fileout,"PaperId,AuthorId,Name,Affiliation"
    for line in filein:
        print >>fileout,line.strip()
        count +=1
        if count == 500000:
            numfile+=1
            count=0
            fileout=open('data/PaperAuthor_%02d.csv'%numfile,'w')
            print >>fileout,"PaperId,AuthorId,Name,Affiliation"
