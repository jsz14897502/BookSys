from django.utils.timezone import now
from LibrarySys import models


class ExpiryTimeTask(object):
    def __init__(self):
        pass

    def request_status_modify(self):
        worked_request_obj_li = models.Request.objects.filter(confirm_code__exact=0)
        for wk_req in worked_request_obj_li:
            time_judge = wk_req.expiry_time < now()
            if time_judge:
                wk_req.confirm_code = 3
            else:
                pass

    def borrow_status_modify(self):
        book_obj_li = models.Book_list.objects.filter(state_code=0)
        worked_borrow_obj_li = models.Borrow.objects.filter(book_name__in=book_obj_li)
        for wk_brr in worked_borrow_obj_li:
            time_judge = wk_brr.end_time < now()
            if time_judge:
                wk_brr.book_name.state_code = 1
                violation = models.Violation_record(user=wk_brr.book_name.owner, book_name=wk_brr.book_name,
                                                    violation_type=1, cretime=now(), treat_state=0)
                violation.save()
            else:
                pass








