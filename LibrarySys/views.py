from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils.timezone import now
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from . import assistant
from . import models
import datetime


def login_required(func):
    def wrapper(request, *args, **kwargs):
        cookie = request.COOKIES
        if "stu_id" in cookie.keys():
            return func(request, *args, **kwargs)
        else:
            return redirect(to=reverse("login"), permanent=False)
    return wrapper


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
        find_user = models.User.objects.filter(stu_id=stu_id, password=password)
        if len(find_user) == 1:
            # 先创建 response
            response = JsonResponse({'msg': '2200'})
            response.set_cookie(key='stu_id', value=stu_id, max_age=(4 * 60 * 60))
            # 记录登录时间
            login_time = now()
            login_time_record = models.Login_record(user=find_user[0], login_time=login_time)
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
        find_user = models.User.objects.filter(stu_id=stu_id)
        if len(find_user) is 0:  # 查询到0条记录，即用户不存在
            # 为用户注册
            new_user = models.User(stu_id=stu_id, user_name=user_name, password=password,
                            email=email, phone=phone, cretime=signup_time, last_time=signup_time)
            new_user.save()
            # 记录该次登录时间
            last_registered_user = models.User.objects.filter(stu_id=stu_id)  # 找到刚刚用这个学号注册的用户
            login_time = signup_time
            login_time_record = models.Login_record(user=last_registered_user[0], login_time=login_time)
            login_time_record.save()
            # 创建 response
            response = JsonResponse({'msg': '2200'})
            response.set_cookie(key='stu_id', value=stu_id, max_age=(4 * 60 * 60))
            return response
        else:
            return JsonResponse({'msg': "4400"})


@ method_decorator([login_required], name='dispatch')
class BookListView(ListView):
    """书籍总页的视图类"""
    model = models.Book_list
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


@ method_decorator([login_required], name='dispatch')
class BookDetailView(View):
    """书籍详情页的视图类"""
    def get(self, request, book_id):
        book = models.Book_list.objects.get(id__exact=book_id)
        owner = models.User.objects.get(id__exact=book.owner.id)
        book_comments = models.Book_short_comment.objects.filter(book=book.id)
        comments = []
        for comment in book_comments:
            message = {}
            message["commentator"] = comment.commentator.user_name
            message["comment_text"] = comment.comment_text
            comments.append(message)
            # print(comment.comment_text)
        context = {
            "book_id": book.id,
            "book_name": book.book_name,
            "isbn": book.isbn,
            "author": book.author,
            "translator": book.translator,
            "press": book.press,
            "price": book.price,
            "profiles": book.profiles,
            "owner": owner.user_name,
            "phone": owner.phone,
            "email": owner.email,
            "borrowed_times": book.borrowed_times,
            "comments": comments
        }
        return render(request, "LibrarySys/detail.html", context=context)

    def post(self, request, book_id):
        # 从前端的 ajax 中获取注册所需数据
        state_code = request.POST.get('state_code')
        # 判断功能创建
        comment_judge = assistant.BookCommentJudge(request)
        borrow_judge = assistant.BorrowJudge(request)
        # 状态码判断
        if state_code == "6698":
            # 操作可行性判断
            if comment_judge.comment_request():
                return JsonResponse({'msg': '2299'})
            else:
                return JsonResponse({'msg': '4498'})
        elif state_code == "6697":
            if comment_judge.submit_comment():
                return JsonResponse({'msg': '2200'})
            else:
                return JsonResponse({'msg': '5599'})
        elif state_code == "6699":
            if borrow_judge.judge(): # 待更改
                print("执行")
                if borrow_judge.borrow_request():
                    print("到这里")
                    return JsonResponse({'msg': '2200'})
                else:
                    return JsonResponse({"msg": "5599"})
            else:
                return JsonResponse({"msg": "5598"})
        else:
            return JsonResponse({'msg': '5599'})


@ method_decorator([login_required], name='dispatch')
class HomePageView(View):
    """个人主页视图函数"""
    def get(self, request):
        context = {}
        stu_id = request.COOKIES["stu_id"]
        req_borr_info = assistant.RequestAndBorrowInfo(request, stu_id)
        # 这是目前借阅到的书的部分的数据
        context.update(req_borr_info.borrowed_books())
        # 这是发出的请求的部分的数据
        context.update(req_borr_info.my_requests())
        # 这是收到的请求的部分的数据
        context.update(req_borr_info.received_requests())
        return render(request, "homepage.html", context=context)

    def post(self, request):
        if request.POST["state_code"] == "6696":
            lend_judge = assistant.LendJudge(request)
            if lend_judge.judge():
                if lend_judge.lend_book():
                    return JsonResponse({"msg": "2299"}) # 执行正常
                else:
                    return JsonResponse({"msg": "5500"}) # 数据库操作异常
            else:
                return JsonResponse({"msg": "4499"}) # 该用户借阅行为异常
        else:
            return JsonResponse({"msg": "5501"}) # 不支持其他请求


def test(request):
    """测试用的，不用管"""
    # find_user = User.objects.filter(stu_id='001', password='python')
    # print(find_user[0].stu_id)
    # find_user = User.objects.filter(stu_id="002", password="python")
    # login_time = now()
    # login_time_record = Login_record(user=find_user[0], login_time=login_time)
    # print(login_time)
    # login_time_record.save()

    # book_id = request.POST.get("book_id")
    # book_id = 1
    # book_obj = models.Book_list.objects.get(id__exact=book_id)
    # comments_li = models.Book_short_comment.objects.filter(book=book_obj)
    # comment_num_today = 0
    # now_time = now()
    # for comment in comments_li:
    #     print(comment)
    #     dd = comment.comment_time.date() > now_time.date()
    #     print(dd)
    #     if comment.comment_time.date() == now_time.date():
    #         comment_num_today += comment_num_today
    # if comment_num_today > 2:
    #     print("can't")
    # else:
    #     print("you can")

    stu_id = "001"
    book_name = "汇编语言 第三版"
    user_obj = models.User.objects.get(stu_id=stu_id)
    book_obj = models.Book_list.objects.get(book_name=book_name)
    vio = models.Violation_record(user=user_obj, book_name=book_obj, violation_type=1, cretime=now())
    # vio.save()
    return HttpResponse("你竟然无聊到试这个... emmmmm....你注销账户吧...........")







