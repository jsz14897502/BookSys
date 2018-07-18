from django.db import models


class book_list(models.Model):
    id = models.AutoField(primary_key=True)
    isbn = models.CharField(max_length=15, null=False)
    book_name = models.CharField(max_length=20, null=False)
    author = models.CharField(max_length=100, null=False)
    translator = models.CharField(max_length=40, null=True)
    press = models.CharField(max_length=20, null=False)
    price = models.IntegerField(null=False)
    owner = models.ForeignKey("user", on_delete=models.DO_NOTHING)
    borrowed_times = models.IntegerField(default=0, null=False)
    state_code = models.IntegerField(default=0, null=False)


class borrow(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.ForeignKey("book_list", on_delete=models.DO_NOTHING)
    owner = models.ForeignKey("user", on_delete=models.DO_NOTHING)
    end_time = models.DateTimeField(null=False)
    previous = models.ForeignKey("user", on_delete=models.DO_NOTHING)


class login_record(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("user", on_delete=models.DO_NOTHING)
    login_time = models.DateTimeField(null=False)


class request(models.Model):
    id = models.AutoField(primary_key=True)
    book_name = models.ForeignKey("book_list", on_delete=models.DO_NOTHING)
    cretime = models.DateTimeField(null=False)
    requester = models.ForeignKey("user", on_delete=models.DO_NOTHING)
    owner = models.ForeignKey("user", on_delete=models.DO_NOTHING)
    confirm_code = models.SmallIntegerField(default=0, null=False)
    expiry_time = models.DateTimeField(null=False)


class user(models.Model):
    id = models.AutoField()
    stu_id = models.CharField(max_length=12, null=False, primary_key=True)
    user_name = models.CharField(max_length=10, null=False)
    password = models.CharField(max_length=16, null=False)
    email = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=14, null=False)
    holds = models.IntegerField(default=0, null=True)
    cretime = models.DateTimeField(null=False)
    last_time = models.DateTimeField(null=True)
    cancellation = models.BooleanField(default=0, null=False)



# class book_list(models.Model):
#     pass

