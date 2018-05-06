from random import choice, randint, random
import math

import numpy as np

from django.contrib.auth.models import User
from questions.models import Question, Post, Reaction


tags = ['c', 'c++', 'python', 'django',  'misc', 'ada', 'algorithms', 'general', 'template', 'detail']
    #    'mock', 'testing', 'nodejs', 'angularjs', 'jquery', 'ai', 'web', 'decorators', 'generators', 'iter']
    #, 'os', 'iot','sql', 'flask', 'pyramid', 'search', 'net', 'cmd', 'ls', 'cp', 'mv', 'bash', 'yarn', 'npm', 'other', 'd']
usernames = ['arian', 'ali', 'hasan', 'mona', 'mahtab', 'bita', 'jack', 'john', 'sheida']

alpha = 0.5
#p_c_zipf = [1. / (math.pow(float(i), alpha)) for i in range(1, len(tags)+1)]
p_c_zipf = [5]*2 + [4]*3 + [3]*4 + [2]*5 + [1]*6
p_c_zipf = np.multiply(1.0/sum(p_c_zipf), p_c_zipf).tolist()


def mock_users():
    print('making mock users')
    for user in usernames:
        User(username=user, password='123not'+user, email=user+'@gmail.com', first_name=user, last_name='jamali').save()


def mock_questions(count=20):
    print('making mock questions')
    us = User.objects.all()
    for i in range(count):
        u = choice(us)
        #stuffs = list(set(choice(tags) for i in range(randint(1, len(tags)-1))))
        stuffs = np.random.choice(tags, randint(0, 5), p=p_c_zipf)
        title = 'title ' + ' '.join(stuffs)
        body = ' '.join(stuffs) + ' body'
        q = Question(author=u, title=title, body=body)
        q.save()
        q.tags.add(*tuple(stuffs))
        q.save()


def mock_posts(count=40):
    print('making mock posts')
    us = User.objects.all()
    qs = Question.objects.all()
    for i in range(count):
        u = choice(us)
        q = choice(qs)
        b = 'You should %d %d'%(i, randint(0,10))
        p = Post(author=u, question=q, body=b)
        p.save()


def mock_reactions(count=400):
    print('making mock reactions')
    qs = Question.objects.all()
    ps = Post.objects.all()
    us = User.objects.all()
    for i in range(count):
        vote = 'm' if random() < 0.2 else 'p'
        u = choice(us)
        if random() > 0.5:
            # question
            obje = 'q'
            q = choice(qs)
            oid = q.id
        else:
            # post
            obje = 'p'
            p = choice(ps)
            oid = p.id
        r = Reaction(oid=oid, obje=obje, vote=vote, author=u)
        r.save()


def mock_complete():
    mock_users()
    mock_questions()
    mock_posts()
    mock_reactions()

