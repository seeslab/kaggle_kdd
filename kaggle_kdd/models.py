__author__ = 'jduch'

from django.db import models

class Journal(models.Model):
    id = models.IntegerField(primary_key=True)
    shortname = models.CharField(blank=True, null=True, max_length=4000)
    fullname = models.CharField(blank=True, null=True, max_length=4000)
    homepage = models.CharField(blank=True, null=True, max_length=4000)


class Conference(models.Model):
    id = models.IntegerField(primary_key=True)
    shortname = models.CharField(blank=True, null=True, max_length=4000)
    fullname = models.CharField(blank=True, null=True, max_length=4000)
    homepage = models.CharField(blank=True, null=True, max_length=4000)


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=4000)
    affiliation = models.CharField(blank=True, null=True, max_length=4000)


class Keywords(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(blank=True, null=True, max_length=4000)


class Paper(models.Model):
    journal = models.ForeignKey(Journal, null=True)
    conference = models.ForeignKey(Conference, null=True)

    id = models.IntegerField(primary_key=True)
    title = models.CharField(blank=True, null=True, max_length=4000)
    year = models.IntegerField(null=True)
    keywords_string = models.CharField(blank=True, null=True, max_length=4000)
    keywords = models.ManyToManyField(Keywords, null=True)


class PaperAuthor(models.Model):
    paper = models.ForeignKey(Paper, null=True)
    author = models.ForeignKey(Author, null=True)

    paperId = models.IntegerField(null=True,blank=True)
    authorId = models.IntegerField(null=True,blank=True)

    name = models.CharField(blank=True, null=True, max_length=4000)
    affiliation = models.CharField(blank=True, null=True, max_length=4000)

