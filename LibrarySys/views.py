from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils.timezone import now
from .models import user, login_record


def login(request):
    """登陆视图函数"""
    return render(request, 'login.html')


def login_check(request):
    """ajax 登录校验回调视图函数"""
    # 1，获取用户输入的用户名和密码
    stu_id = request.POST.get('stu_id')
    password = request.POST.get('password')

    # 2,用户名和密码校验以及记录登录时间
    find_user = user.objects.filter(stu_id=stu_id, password=password)
    if len(find_user) is 1:
        # 先创建 response
        response = JsonResponse({'msg': 'success'})
        response.set_cookie(key='stu_id', value=stu_id, max_age=(4 * 60 * 60))
        # 记录登录时间
        user_id = find_user[0].id
        login_time = now()
        login_time_record = login_record(user=user_id, login_time=login_time)
        login_time_record.save()

        return response
    else:
        response = JsonResponse({'msg': 'error'})
        return response


def register(request):
    """注册按钮视图函数"""
    return render(request, 'register.html')


def register_check(request):
    """ajax 注册校验视图函数"""
    # 从前端的 ajax 中获取注册所需数据
    stu_id = request.POST.get('stu_id')
    user_name = request.POST.get('user_name')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    # 进行用户存在判断
    signup_time = now()
    find_user = user.objects.filter(stu_id=stu_id)
    if len(find_user) is 0: # 查询到0条记录，即用户不存在
        # 为用户注册
        new_user = user(stu_id=stu_id, user_name=user_name, password=password,
                        email=email, phone=phone, cretime=signup_time, last_time=signup_time)
        new_user.save()
        # 记录该次登录时间
        last_registered_user = user.objects.filter(stu_id=stu_id) # 找到刚刚用这个学号注册的用户
        user_id = last_registered_user[0].id # 获取这个用户的 id
        login_time = signup_time
        login_time_record = login_record(user=user_id, login_time=login_time)
        login_time_record.save()
        # 创建 response
        response = JsonResponse({'msg': 'success'})
        response.set_cookie(key='stu_id', value=stu_id, max_age=(4*60*60))
        return response
    else:
        return JsonResponse({'msg': "stu_id_error"})


def index(request):
    """首页视图函数"""
    cookie = request.COOKIES
    if len(cookie) is 0:
        return render(request, 'login.html')
    else:
        return render(request, 'index.html')


def test(request):
    """测试用的，不用管"""
    # find_user = user.objects.filter(stu_id='001', password='python')
    # print(find_user[0].stu_id)
    return HttpResponse("shit....")

