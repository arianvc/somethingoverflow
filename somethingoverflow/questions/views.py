# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import string

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User, Group
from .models import Question, Post, Reaction
from .forms import LoginForm, RegisterForm, RecoverForm, NewPostForm, AnswerForm

# Handy functions
random_str = lambda N: ''.join(
    random.SystemRandom().choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))


# Create your views here.

def log_in(request, **kwargs):
    context = { 'message':kwargs['message'] if 'message' in kwargs else 'Welcome!',
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
                    return redirect('tasks')#TODO, message=context['message'])
                else:
                    context['message'] = 'Disabled account'
            else:
                context['message'] = 'Invalid login'
        else:
            form = LoginForm()
    return render(request, 'login.html', context)


def questions(request):
    pass


def ask(request):
    pass


def answer(request):
    pass


def react(request):
    pass
