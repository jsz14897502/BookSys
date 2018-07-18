from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'register.html')

def index(request):
    pass