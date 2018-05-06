# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, string, threading
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from taggit.models import Tag

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image

from .models import Question, Post, Reaction
from .forms import LoginForm, RegisterForm, RecoverForm, QuestionForm, PostForm

# Handy functions
random_str = lambda N: ''.join(
    random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# Register and activation
def register(request):
    message = 'Bad register request' #TODO pass this
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            if len(User.objects.filter(username=username)) != 0:
                message = 'Username exists! Choose a different one!'
            else:
                password = cd.get('password')
                email = cd.get('email') #TODO: should be unique!
                first_name = cd.get('first_name')
                last_name = cd.get('last_name')
                user = User.objects.create_user(username=username, password=password, email=email,
                                                first_name=first_name, last_name=last_name)
                user.is_active = False
                if user:
                    user.save()
                    date = str(user.date_joined)
                    print(date + email + settings.SECRET_KEY)
                    print(hash(date + email + settings.SECRET_KEY))
                    send_mail('Somethingoverflow account activation',
                              'http://127.0.0.1:8000/activate?username=%s&&code=%s' %
                              (username, hash(date + email + settings.SECRET_KEY)),
                              'info@somethingoverflow.com',
                              [email],
                              )
                    message = 'Check your email at ' + email
                else:
                    message = 'Error creating user'
    request.method = 'GET' #TODO: there must be a better way!
    return log_in(request, message=message) #TODO: redirect with parameters


def activate(request):
    message = 'Wrong activation link, please try again'
    #data = request.GET
    #if 'username' in data and 'code' in data:
    username = request.GET.get('username', '')
    code = request.GET.get('code', '')
    if username and code:
        user = User.objects.get(username=username)
        email = user.email
        date = str(user.date_joined)
        print(username, date, email)
        print(date + email + settings.SECRET_KEY)
        print(int(code), ' vs ', hash(date+email+settings.SECRET_KEY))
        if hash(date+email+settings.SECRET_KEY) == int(code):
            user.is_active = True
            user.save()
            message = 'You have successfully created an account, now you can log in.'
    return log_in(request, message=message)


## Logging in and out
def log_in(request, **kwargs):
    context = {'message': kwargs['message'] if 'message' in kwargs else 'Welcome!',
               'loginform': LoginForm,
               'registerform': RegisterForm,
               'recoverform': RecoverForm,
               }
    if request.user.is_authenticated:
        return redirect('questions')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('questions')  # Profile? Console?
                else:
                    context['message'] = 'Disabled account'
            else:
                context['message'] = 'Invalid login'
        else:
            form = LoginForm() #?
    return render(request, 'login.html', context)


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/login')


def questions(request, tag_slug=None, page=0):
    page = int(page)
    question_list = Question.objects.order_by("-created")
    #TODO: paged!
    if request.method == 'POST':
        # new question
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.author = request.user
            q.save()
            form.save_m2m()
            redirect('question', qid=q.id)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        question_list = question_list.filter(tags__in=[tag])

    context = {'questions': question_list[page*10:(page+1)*10],
               'questionform': QuestionForm,
               }
    return render(request, 'questions.html', context)


def question(request, qid=None, action=None):
    if request.method == 'GET':
        if 'qid' not in request.GET:
            raise Http404()
    elif request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
        print('new post', qid)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                f = form.cleaned_data
                f['author'] = request.user
                f['question'] = Question.objects.get(id=qid)
                q = Post(**f)
                q.save()
    actions = {'upvote': '', 'downvote': '', 'delete': '', 'edit': '', }
    if action in actions:
        if action == 'edit':
            redirect(action, etype='question', eid=qid)
        elif action == 'delete':
            Question.objects.filter(id=qid).delete()
        elif action == 'upvote' or action == 'downvote':
            vote = {'upvote': 'p', 'downvote': 'm'}[action]
            author = request.user
            if 'pid' not in request.GET:
                # Question
                obje = 'q'
                oid = qid
            else:
                pid = request.GET['pid']
                obje = 'p'
                oid = pid
            r = Reaction(vote=vote, author=author, oid=oid, obje=obje)
            r.save()
            pass
        else:
            raise Http404()
    posts = Post.objects.filter(question__id=qid).order_by("-created")
    for post in posts:
        score = 0
        sc = Reaction.objects.filter(post=post).values('status').annotate(rcount=Count('status'))
        for rt in sc:
            if rt['status'] == 'm':
                score -= rt['rcount']
            if rt['status'] == 'p':
                score += rt['rcount']
        post.score = score
        post.owner = request.user == post.author
    the_question = Question.objects.get(id=qid)
    the_question.owner = the_question.author == request.user
    context = {'question': the_question,
               'posts': posts,
               'postform': PostForm,
               }
    return render(request, 'question.html', context)


def tags_view(request):
    def refresh_image(wd):
        wordlist = list()
        for w in wd:
            for i in range(wd[w]):
                wordlist.append(w.name)
        np.random.shuffle(wordlist)
        print(type(wordlist))
        text = ' '.join(wordlist)
        #print(text)
        basepath = os.path.abspath(os.path.dirname(__file__))
        # imgpath = basepath + "/static/tag_cloud_mask2.jpg"
        outpath = basepath + '/static/tags_cloud.png'
        text = (text)
        # wave_mask = np.array(Image.open(imgpath))
        # wordcloud = WordCloud(width=1280, height=720, mask=wave_mask, max_font_size=40, background_color="white").generate(text)
        wordcloud = WordCloud(width=640, height=480, background_color="white").generate(text)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.margins(x=0, y=0)
        plt.savefig(outpath)
    queryset = Tag.objects.all()
    queryset = queryset.annotate(hit=Count('taggit_taggeditem_items'))
    taghit = dict()
    for tag in queryset:
        taghit[tag] = tag.hit
    #refresh_image(taghit)
    context = {'taghit': taghit,
               }
    return render(request, 'tags.html', context)


def general_edit(request, etype=None, eid=None):
    if etype == 'question':
        this = Question.objects.get(id=eid)
    elif etype == 'post':
        this = Post.objects.get(id=eid)
    else:
        raise Http404()
    owner = request.user == this.author
    if not owner:
        raise HttpResponseForbidden()
    context = {'etype': etype,
               }
    forms = {'question': QuestionForm,
             'post': PostForm}
    form = forms[etype]
    if request.method == 'GET':
        context['form'] = form(instance=this)
        return render(request, "edit.html", context)

    elif request.method == 'POST':
        form = form(request.POST or None, instance=this)
        if form.is_valid():
            form.save()
        redirect(etype, eid)
    else:
        return Http404()


def edit_post(request, pid):
    print('shit', pid)
    return HttpResponse('works dude! move on!')


def profile(request):
    pass
