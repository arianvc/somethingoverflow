# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

dict2tuple4sqlenum = lambda da_dict: tuple((k, da_dict[k]) for k in da_dict)


# Create your models here.

class Question(models.Model):
    def __str__(self):
        return '{} - {} by {}'.format(self.id, self.title, self.author)
    author = models.ForeignKey(User, related_name='questions_by', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    tags = TaggableManager()


class Post(models.Model):
    def __str__(self):
        return '{} Post {}... for '.format(self.id, self.body[:10], self.question.title)
    created = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, related_name='questions_by', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts_by', on_delete=models.CASCADE)
    body = models.TextField()


class Reaction(models.Model):  # TODO: not efficient, what's the alternative?
    class Meta:
        unique_together = (('obje', 'author', 'oid'), )

    def __str__(self):
        thing = self.OBJE[self.obje] + str(self.oid)
        return '{}:{}:{}'.format(self.author, thing, self.vote)
    VOTE = {'p': 'Plus', 'm': 'Minus'}
    OBJE = {'q': 'Question', 'p': 'POST'}
    oid = models.IntegerField(default=-1)
    obje = models.CharField(max_length=1, default='p', choices=dict2tuple4sqlenum(OBJE))
    vote = models.CharField(max_length=1, default='p', choices=dict2tuple4sqlenum(VOTE))
    #post = models.ForeignKey(Post, related_name='reactions_for_post', null=True, blank=True, on_delete=models.CASCADE)
    #question = models.ForeignKey(Question, related_name='reactions_for_question', null=True, blank=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='reactions_by', on_delete=models.CASCADE)
    # TODO: SHOULD BE UNIQUE

# TODO: comment
