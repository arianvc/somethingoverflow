# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


dict2tuple4sqlenum = lambda da_dict: tuple((k, da_dict[k]) for k in da_dict)


# Create your models here.

class Question(models.Model):
    def __str__(self):
        return '{} by {} from {}'.format(self.id, self.title, self.author)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='questions_by')


class Post(models.Model):
    def __str__(self):
        return '{} by {} from {}'.format(self.id, self.title, self.author)
    body = models.TextField()
    question = models.ForeignKey(Question, related_name='questions_by')


class Reaction(models.Model):  # TODO: not efficient, what's the alternative
    def __str__(self):
        return '{} by {} from {}'.format(self.id, self.title, self.author)
    TYPE = {'p':'Plus', 'm':'Minus'}
    status = models.CharField(max_length=1, default='p', choices=dict2tuple4sqlenum(TYPE))
    post = models.ForeignKey(Post, related_name='reactions_for')
    author = models.ForeignKey(User, related_name='posts_by')

# TODO: comment
