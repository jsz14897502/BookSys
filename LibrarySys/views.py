from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .models import user
import datetime
import base64


# ajax 登陆视图函数
def login(request):
    return render(request, 'login.html')


# ajax 登录校验回调视图函数
def login_check(request):
    # 1，获取用户输入的用户名和密码
    stu_id = request.POST.get('stu_id')
    password = request.POST.get('password')
    # 2,用户名和密码校验
    find_user = user.objects.filter(stu_id=stu_id, password=password)
    if len(find_user) is 1:
        response = JsonResponse({'msg': 'success'})
        response.set_cookie(key='stu_id', value=stu_id, max_age=(4 * 60 * 60))
        return response
    else:
        response = JsonResponse({'msg': 'error'})
        return response


def register(request):
    return render(request, 'register.html')


def register_check(request):
    stu_id = request.POST.get('stu_id')
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    now = datetime.datetime.now()
    find_user = user.objects.filter(stu_id=stu_id)
    if len(find_user) is 0:
        new_user = user(stu_id=stu_id, user_name=user_name, password=password,
                        email=email, phone=phone, cretime=now, last_time=now)
        new_user.save()
        response = JsonResponse({'msg': 'success'})
        response.set_cookie(key='stu_id', value=stu_id, max_age=(4*60*60))
        return response
    else:
        return JsonResponse({'msg': "stu_id_error"})


def index(request):
    cookie = request.COOKIES
    if len(cookie) is 0:
        return render(request, 'login.html')
    else:
        return render(request, 'index.html')


def test(request):
    # find_user = user.objects.filter(stu_id='001', password='python')
    # print(find_user[0].stu_id)
    return HttpResponse("shit....")

