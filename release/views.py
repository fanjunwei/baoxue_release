# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
import datetime
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from release.helper import *
# Create your views here.
from django.template.response import TemplateResponse


def login(request):
    next = request.REQUEST.get('next', '')
    if request.method == 'POST':
        username = request.REQUEST.get('username')
        password = request.REQUEST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse(home))
        else:
            messages.error(request, '用户名或密码错误')
    else:
        users = User.objects.all()
        if users.count() == 0:
            user = User()
            user.username = 'SW'
            user.set_password('SW')
            user.is_superuser = True
            user.save()

    return TemplateResponse(request, 'login.html', locals())


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse(login))


@login_required
def home(request):
    return TemplateResponse(request, 'home.html', locals())


@login_required
def branch_manage(request):
    if request.method == 'POST':
        branch = request.REQUEST.get('branch')
        description = request.REQUEST.get('description')

    return TemplateResponse(request, 'branch_manage.html', locals())


def upload(request):
    files = request.FILES.items()
    print(files)
