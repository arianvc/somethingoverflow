# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User, Group
from .models import Question, Post, Reaction
from .forms import LoginForm, RegisterForm, RecoverForm, QuestionForm, PostForm

# Handy functions
random_str = lambda N: ''.join(
    random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# Create your views here.

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
                    return redirect('tasks')  # TODO, message=context['message'])
                else:
                    context['message'] = 'Disabled account'
            else:
                context['message'] = 'Invalid login'
        else:
            form = LoginForm()
    return render(request, 'login.html', context)


# TODO: @login_required
def questions(request):
    if request.method == 'POST':
        # new question
        form = QuestionForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            f['author'] = request.user
            q = Question(**f)
            q.save()
            redirect('question', qid=q.id)

    context = {'questions': Question.objects.order_by("-created")[:10],
               'questionform': QuestionForm,
               }
    return render(request, 'questions.html', context)


def question(request, qid=None):
    if qid == None:
        qid = Question.objects.first().id
    if request.method == 'POST':
        print('new question', qid)
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                f = form.cleaned_data
                f['author'] = request.user
                f['question'] = Question.objects.get(id=qid)
                q = Post(**f)
                q.save()
    posts = Post.objects.filter(question__id=qid).order_by("-created")
    context = {'question': Question.objects.get(id=qid),
               'posts': posts,
               'postform': PostForm,
               }
    return render(request, 'question.html', context)


def edit_question(request, qid):
    pass


def edit_post(request, pid):
    pass


def react(request, rtype, rid, reaction): # TODO: uniqueness
    react_dict = {'up':'p', 'down':'m'}
    p = None
    q = None
    if rtype == 'q':
        q = Question.objects.get(id=rid)
        out = redirect('question', qid=rid)
    elif rtype == 'p':
        p = Post.objects.get(id=rid)
        out = redirect('question', qid=p.question.id)
    else:
        out = HttpResponse('Wrong reaction type')
    r = Reaction(status=react_dict[reaction], post=p, question=q, author=request.user)
    r.save()
    return out

