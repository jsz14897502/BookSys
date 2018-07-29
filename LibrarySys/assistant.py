from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.utils.timezone import now
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from . import models
import datetime


class BorrowJudge():
    def __init__(self, request):
        self.request = request
        self.stu_id = request.COOKIES["stu_id"]

    def judge(self):
        if self.viloation_constraint() and self.request_and_holds_constraint():
            return True
        else:
            return False

    def borrow_request(self):
        book_id = self.request.POST.get("book_id")
        stu_id = self.request.COOKIES.get("stu_id")
        book_obj = models.Book_list.objects.get(id__exact=book_id)
        requester_obj = models.User.objects.get(stu_id=stu_id)
        expiry_time = now() + datetime.timedelta(days=2)
        request_record = models.Request(book_name=book_obj, cretime=now(),
                                        requester=requester_obj, expiry_time=expiry_time)
        try:
            request_record.save()
            return True
        except:
            return False

    def request_and_holds_constraint(self):
        user_obj = models.User.objects.get(stu_id=self.stu_id)
        worked_requests_obj_li = models.Request.objects.filter(requester=user_obj, confirm_code__exact=0)
        worked_req_num = len(worked_requests_obj_li)
        holds_num = user_obj.holds
        if (worked_req_num + holds_num) >= 3:
            return False
        else:
            return True

    def viloation_constraint(self):
        user_obj = models.User.objects.get(stu_id=self.stu_id)
        violation_record_obj_li = models.Violation_record.objects.filter(user=user_obj, treat_state=0)
        if len(violation_record_obj_li) > 0:
            return False
        else:
            return True


class LendJudge():
    def __init__(self, request):
        self.request = request

    def judge(self):
        if self.violation_constraint():
            return True
        else:
            return False

    def lend_book(self):
        stu_id = self.request.COOKIES["stu_id"]
        bookname_tobe_borrowed = self.request.POST["book_name"]
        requester_dataid = self.request.POST["user_data_id"]
        requester_obj = models.User.objects.get(id__exact=requester_dataid)
        user_obj = models.User.objects.get(stu_id=stu_id)
        book_obj = models.Book_list.objects.get(owner=user_obj, book_name=bookname_tobe_borrowed)
        end_time = now() + datetime.timedelta(days=10)
        borrow_record = models.Borrow(book_name=book_obj, end_time=end_time, previous=user_obj)
        refuse_part = LinkagePart(self.request)
        try:
            borrow_record.save()
            book_obj.owner = requester_obj
            refuse_part.refuse_other_request_while_lend()
            return True
        except:
            return False

    def violation_constraint(self):
        stu_id = self.request.COOKIES["stu_id"]
        user_obj = models.User.objects.get(stu_id=stu_id)
        violation_record_li = models.Violation_record.objects.filter(user=user_obj,
                                                                     violation_type__in=[1, 2, 3], treat_state=0)
        if len(violation_record_li) == 0:
            return True
        else:
            return False


class BookCommentJudge():
    def __init__(self, request):
        self.request = request

    def comment_request(self):
        book_id = self.request.POST.get("book_id")
        book_obj = models.Book_list.objects.get(id__exact=book_id)
        comments_li = models.Book_short_comment.objects.filter(book=book_obj)
        comment_num_today = 0
        now_time = now()
        for comment in comments_li:
            if comment.comment_time.date() == now_time.date():
                comment_num_today = comment_num_today + 1
        if comment_num_today > 2:
            return False
        else:
            return True

    def submit_comment(self):
        book_id = self.request.POST.get("book_id")
        stu_id = self.request.COOKIES.get("stu_id")
        comment_text = self.request.POST.get("comment_text")
        book_obj = models.Book_list.objects.get(id__exact=book_id)
        commentator = models.User.objects.get(stu_id__exact=stu_id)
        new_comment = models.Book_short_comment(book=book_obj, commentator=commentator,
                                                comment_text=comment_text, comment_time=now())
        try:
            new_comment.save()
            return True
        except:
            return False


class RequestAndBorrowInfo():
    def __init__(self, request, stu_id):
        self.request = request
        self.stu_id = stu_id

    def borrowed_books(self):
        user_obj = models.User.objects.filter(stu_id=self.stu_id)
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

    def my_requests(self):
        user_obj = models.User.objects.get(stu_id=self.stu_id)
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

    def received_requests(self):
        user_obj = models.User.objects.get(stu_id=self.stu_id)
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
                wk_re["user_data_id"] = worked_req.requester.id
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


class LinkagePart():
    def __init__(self, request):
        self.request = request

    def refuse_other_request_while_lend(self):
        book_name = self.request.POST["book_name"]
        book_obj = models.Book_list.objects.get(book_name__exact=book_name)
        worked_request_li = models.Request.objects.filter(book_name__exact=book_obj, confirm_code__exact=0)
        for wk_req in worked_request_li:
            wk_req.confirm_code = 2






