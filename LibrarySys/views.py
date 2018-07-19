from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'register.html')


def index(request):
    return render(request, 'index.html')


def accounts_login(request):
    return HttpResponse("登陆中")


def accounts_signup(request):
    return HttpResponse("注册中")
