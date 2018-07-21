from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils.timezone import now
from .models import user, login_record, book_list


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
        response = JsonResponse({'msg': '2200'})
        response.set_cookie(key='stu_id', value=stu_id, max_age=(4 * 60 * 60))
        # 记录登录时间
        login_time = now()
        login_time_record = login_record(user=find_user[0], login_time=login_time)
        login_time_record.save()

        return response
    else:
        response = JsonResponse({'msg': '4499'})
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
        login_time = signup_time
        login_time_record = login_record(user=last_registered_user[0], login_time=login_time)
        login_time_record.save()
        # 创建 response
        response = JsonResponse({'msg': '2200'})
        response.set_cookie(key='stu_id', value=stu_id, max_age=(4*60*60))
        return response
    else:
        return JsonResponse({'msg': "4400"})


def index(request):
    """首页视图函数"""
    cookie = request.COOKIES
    if len(cookie) is 0:
        return render(request, 'login.html')
    else:
        context = {}
        book_num = book_list.objects.all().count()
        context["book_num"] = book_num
        context["books"] = []

        page_num = int(request.GET.get("page_num"))
        book_id_num = [(page_num*8 - 7), (page_num*8 - 6), (page_num*8 - 5), (page_num*8 - 4),
                       (page_num*8 - 3), (page_num*8 - 2), (page_num*8 - 1), (page_num*8)]
        books = book_list.objects.filter(id__in=book_id_num)
        for book in books:
            book_detail = {}
            book_detail["book_name"] = book.book_name
            book_detail["author"] =  book.author
            book_detail["translator"] = book.translator
            book_detail["isbn"] = book.isbn
            book_detail["press"] = book.press
            book_detail["profiles"] = book.profiles
            context["books"].append(book_detail)
        print(context)
        return render(request, 'index.html', context=context)


def test(request):
    """测试用的，不用管"""
    # find_user = user.objects.filter(stu_id='001', password='python')
    # print(find_user[0].stu_id)
    # find_user = user.objects.filter(stu_id="002", password="python")
    # login_time = now()
    # login_time_record = login_record(user=find_user[0], login_time=login_time)
    # print(login_time)
    # login_time_record.save()
    # dictionary = {'book_num': 3,
    #               1: ['汇编语言 第三版', '王爽', None, '9787302333142', '清华大学出版社', None],
    #               2: ['数据库系统概念 第六版', 'Abraham Silberschatz; Henry F. Korth; S. Sudarshan',
    #                   '杨冬青 李红燕 唐世渭', '9787111400851', '机械工业出版社', None],
    #               3: ['托马斯微积分 第十版', 'Finney; Weir; Giordano', '叶其孝 王耀东 唐兢', '9787040108231', '高等教育出版社', None]}
    # for item in dictionary.items():
    #     print(item)
    #     # if item.key == "book_num":
    #     #     pass
    #     # else:
    #     #     print(item.value)
    return HttpResponse("shit....")

