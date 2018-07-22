from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils.timezone import now
from .models import User, Login_record, Book_list
from django.views.generic import ListView
from django.utils.decorators import method_decorator


def login_required(func):
    def wrapper(request, *args, **kwargs):
        cookie = request.COOKIES
        if cookie["stu_id"] is not None:
            return wrapper(request, *args, **kwargs)
        else:
            return redirect(to=reverse("login"), permanent=False)
    return wrapper()


class DomainView(View):
    """域名视图类"""
    def get(self, request, *args, **kwargs):
        return redirect(to=reverse("login"), permanent=False)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("不支持除 get 之外的其他请求")


class LoginView(View):
    """登陆视图类"""
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        """ajax 登录校验回调函数"""
        # 1，获取用户输入的用户名和密码
        stu_id = request.POST.get('stu_id')
        password = request.POST.get('password')
        # 2,用户名和密码校验以及记录登录时间
        find_user = User.objects.filter(stu_id=stu_id, password=password)
        if len(find_user) is 1:
            # 先创建 response
            response = JsonResponse({'msg': '2200'})
            response.set_cookie(key='stu_id', value=stu_id, max_age=(4 * 60 * 60))
            # 记录登录时间
            login_time = now()
            login_time_record = Login_record(user=find_user[0], login_time=login_time)
            login_time_record.save()
            return response
        else:
            response = JsonResponse({'msg': '4499'})
            return response


class RegisterView(View):
    """注册视图类"""
    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        """ajax 注册校验回调函数"""
        # 从前端的 ajax 中获取注册所需数据
        stu_id = request.POST.get('stu_id')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # 进行用户存在判断
        signup_time = now()
        find_user = User.objects.filter(stu_id=stu_id)
        if len(find_user) is 0:  # 查询到0条记录，即用户不存在
            # 为用户注册
            new_user = User(stu_id=stu_id, user_name=user_name, password=password,
                            email=email, phone=phone, cretime=signup_time, last_time=signup_time)
            new_user.save()
            # 记录该次登录时间
            last_registered_user = User.objects.filter(stu_id=stu_id)  # 找到刚刚用这个学号注册的用户
            login_time = signup_time
            login_time_record = Login_record(user=last_registered_user[0], login_time=login_time)
            login_time_record.save()
            # 创建 response
            response = JsonResponse({'msg': '2200'})
            response.set_cookie(key='stu_id', value=stu_id, max_age=(4 * 60 * 60))
            return response
        else:
            return JsonResponse({'msg': "4400"})


@ method_decorator([login_required], name='dispatch')
class BookListView(ListView):
    """用来渲染book.html里的数据的列表视图类"""
    model = Book_list
    template_name = 'book.html'
    paginate_by = 8
    context_object_name = 'books'
    ordering = 'id'
    page_kwarg = 'p'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(*kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        pagination_data = self.get_pagination_data(paginator, page_obj, 3)
        context.update(pagination_data)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page+1, num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1, current_page+around_count+1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }


def test(request):
    """测试用的，不用管"""
    # find_user = User.objects.filter(stu_id='001', password='python')
    # print(find_user[0].stu_id)
    # find_user = User.objects.filter(stu_id="002", password="python")
    # login_time = now()
    # login_time_record = Login_record(user=find_user[0], login_time=login_time)
    # print(login_time)
    # login_time_record.save()
    return HttpResponse("emmmmm... 你竟然无聊到了试这个....你注销账户吧...........")



