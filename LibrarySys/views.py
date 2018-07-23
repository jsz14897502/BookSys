from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils.timezone import now
from django.views.generic import ListView
from django.utils.decorators import method_decorator
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
        # 状态码判断
        if state_code == "6698":
            # 操作可行性判断
            if self.comment_request(request):
                return JsonResponse({'msg': '2299'})
            else:
                return JsonResponse({'msg': '4498'})
        elif state_code == "6697":
            if self.submit_comment(request):
                return JsonResponse({'msg': '2200'})
            else:
                return JsonResponse({'msg': '5599'})
        elif state_code == "6699":
            if self.borrow_request(request):
                return JsonResponse({'msg': '2200'})
        else:
            return JsonResponse({'msg': '5599'})

    def comment_request(self, request):

        book_id = request.POST.get("book_id")
        book_obj = models.Book_list.objects.get(id__exact=book_id)
        comments_li = models.Book_short_comment.objects.filter(book=book_obj)
        comment_num_today = 0
        now_time = now()
        for comment in comments_li:
            if comment.comment_time.date() == now_time.date():
                comment_num_today = comment_num_today + 1
        if comment_num_today > 2:
            return 0
        else:
            return 1

    def submit_comment(self, request):
        book_id = request.POST.get("book_id")
        stu_id = request.COOKIES.get("stu_id")
        comment_text = request.POST.get("comment_text")
        book_obj = models.Book_list.objects.get(id__exact=book_id)
        commentator = models.User.objects.get(id__exact=stu_id)
        new_comment = models.Book_short_comment(book=book_obj, commentator=commentator,
                                                comment_text=comment_text, comment_time=now())
        try:
            new_comment.save()
            return 1
        except:
            return 0

    def borrow_request(self, request):
        book_id = request.POST.get("book_id")
        stu_id = request.COOKIES.get("stu_id")
        book_obj = models.Book_list.objects.get(id__exact=book_id)
        requester_obj = models.User.objects.get(stu_id=stu_id)
        expiry_time = now() + datetime.timedelta(days=2)
        request_record = models.Request(book_name=book_obj, cretime=now(),
                                        requester=requester_obj, expiry_time=expiry_time)
        try:
            request_record.save()
            return 1
        except:
            return 0


@ method_decorator([login_required], name='dispatch')
class HomePageView(View):
    def get(self, request):
        context = {}
        stu_id = request.COOKIES["stu_id"]
        # 这是目前借阅到的书的部分的数据
        context.update(self.borrowed_books(request, stu_id))
        # 这是发出的请求的部分的数据
        context.update(self.my_requests(request, stu_id))
        # 这是收到的请求的部分的数据
        context.update(self.received_requests(request, stu_id))
        return render(request, "homepage.html", context=context)

    def post(self, request):
        pass

    def borrowed_books(self, request, stu_id):
        user_obj = models.User.objects.filter(stu_id=stu_id)
        book_obj_li = models.Book_list.objects.filter(owner=user_obj[0])
        borrows = []
        message_id = 1
        for book in book_obj_li:
            if book.state_code == 1:
                state = "逾期"
            elif book.state_code == 0:
                state = "正常"
            else:
                state = "error"
            borrow_obj_li = models.Borrow.objects.filter(book_name=book)
            borrow_obj_li_len = len(borrow_obj_li)
            borrow_obj = borrow_obj_li[(borrow_obj_li_len - 1)]
            return_time_tuple = borrow_obj.end_time.timetuple()
            return_time = "{}/{}/{}".format(return_time_tuple.tm_year,
                                            return_time_tuple.tm_mon, return_time_tuple.tm_mday)
            borrow_detail = {}
            borrow_detail["message_id"] = message_id
            borrow_detail["book_name"] = book.book_name
            borrow_detail["return_time"] = return_time
            borrow_detail["book_status"] = state
            borrows.append(borrow_detail)
            message_id += 1
        context = {
            "borrows": borrows,
        }
        return context

    def my_requests(self, request, stu_id):
        user_obj = models.User.objects.get(stu_id=stu_id)
        worked_req_li = []
        unworked_req_li = []
        worked_requests_obj_li = models.Request.objects.filter(requester=user_obj, confirm_code__exact=0)
        for worked_req in worked_requests_obj_li:
            expiry_time = self.awaretime_to_date(worked_req.expiry_time)
            cre_time = self.awaretime_to_date(worked_req.cretime)
            wk_re = {}
            wk_re["book_name"] = worked_req.book_name.book_name
            wk_re["owner"] = worked_req.book_name.owner.user_name
            wk_re["cretime"] = cre_time
            wk_re["contact"] = worked_req.book_name.owner.phone
            wk_re["expiry_time"] = expiry_time
            wk_re["state"] = "待审核"
            worked_req_li.append(wk_re)

        unworked_requests_obj_li = models.Request.objects.filter(requester=user_obj, confirm_code__in=[2, 3])
        for unworked_req in unworked_requests_obj_li:
            expiry_time = self.awaretime_to_date(unworked_req.expiry_time)
            cre_time = self.awaretime_to_date(unworked_req.cretime)
            wk_re = {}
            wk_re["book_name"] = worked_req.book_name.book_name
            wk_re["owner"] = worked_req.book_name.owner.user_name
            wk_re["cretime"] = cre_time
            wk_re["contact"] = worked_req.book_name.owner.phone
            wk_re["expiry_time"] = expiry_time
            if unworked_req.confirm_code == 2:
                wk_re["state"] = "拒绝外借"
            else:
                wk_re["state"] = "请求超时"
            unworked_req_li.append(wk_re)
        context = {
            "worked_req": worked_req_li,
            "unworked_req": unworked_req_li,
        }
        return context

    def received_requests(self, request, stu_id):
        user_obj = models.User.objects.get(stu_id=stu_id)
        book_obj_li = models.Book_list.objects.filter(owner=user_obj)
        rec_worked_req_li = []
        rec_unworked_req_li = []
        context_mid_li = []
        req_num = 1
        for book in book_obj_li:
            worked_request_li = models.Request.objects.filter(book_name=book, confirm_code__exact=0)
            for worked_req in worked_request_li:
                expiry_time = self.awaretime_to_date(worked_req.expiry_time)
                cre_time = self.awaretime_to_date(worked_req.cretime)
                wk_re = {}
                wk_re["message_num"] = req_num
                wk_re["requester"] = worked_req.requester.user_name
                wk_re["contact"] = worked_req.requester.phone
                wk_re["cretime"] = cre_time
                wk_re["expiry_time"] = expiry_time
                rec_worked_req_li.append(wk_re)
                req_num += 1
            unworked_request_li = models.Request.objects.filter(book_name=book, confirm_code__in=[2, 3])
            for unworked_req in unworked_request_li:
                expiry_time = self.awaretime_to_date(unworked_req.expiry_time)
                cre_time = self.awaretime_to_date(unworked_req.cretime)
                unwk_re = {}
                unwk_re["requester"] = worked_req.requester.user_name
                unwk_re["contact"] = worked_req.requester.phone
                unwk_re["cretime"] = cre_time
                unwk_re["expiry_time"] = expiry_time
                if unworked_req.confirm_code == 2:
                    unwk_re["reason"] = "拒绝外借"
                else:
                    unwk_re["reason"] = "请求超时"
                rec_unworked_req_li.append(unwk_re)
            context_mid = {
                "book_name": book.book_name,
                "rec_worked_req": rec_worked_req_li,
                "rec_unworked_req": rec_unworked_req_li,
            }
            context_mid_li.append(context_mid)
        context = {
            "rec_reqs": context_mid_li,
        }
        return context

    def awaretime_to_date(self, awaretime):
        time_tuple = awaretime.timetuple()
        time = "{}/{}/{}".format(time_tuple.tm_year, time_tuple.tm_mon, time_tuple.tm_mday)
        return time


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
    book_id = 1
    book_obj = models.Book_list.objects.get(id__exact=book_id)
    comments_li = models.Book_short_comment.objects.filter(book=book_obj)
    comment_num_today = 0
    now_time = now()
    for comment in comments_li:
        print(comment)
        if comment.comment_time.date() == now_time.date():
            comment_num_today += comment_num_today
    if comment_num_today > 2:
        print("can't")
    else:
        print("you can")

    return HttpResponse("emmmmm... 你竟然无聊到了试这个....你注销账户吧...........")







