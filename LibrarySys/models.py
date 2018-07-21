from django.db import models


class Book_list(models.Model):
    """书籍信息表"""
    id = models.AutoField(primary_key=True) # 这条记录的 id，也就是这本书的 id
    isbn = models.CharField(max_length=15, null=False) # 书籍的 isbn
    book_name = models.CharField(max_length=20, null=False) # 书籍名称
    author = models.CharField(max_length=100, null=False) # 书籍作者
    translator = models.CharField(max_length=40, null=True) # 书籍译者
    press = models.CharField(max_length=20, null=False) # 书籍出版社
    price = models.FloatField(null=False) # 书籍价格
    owner = models.ForeignKey("User", on_delete=models.DO_NOTHING) # 书籍所有者的 id
    borrowed_times = models.IntegerField(default=0, null=False) # 书籍被借次数
    state_code = models.IntegerField(default=0, null=False) # 书籍状态码
    profiles = models.CharField(max_length=300, null=True) # 书籍简介
    book_image = models.ImageField(upload_to="%Y/%m/%d/", null=True) # 书籍图片


class Borrow(models.Model):
    """借阅成功记录表"""
    id = models.AutoField(primary_key=True) # 这条记录的 id
    book_name = models.ForeignKey("Book_list", on_delete=models.DO_NOTHING) # 被借书籍的 id
    end_time = models.DateTimeField(null=False) # 借阅结束时间
    previous = models.ForeignKey("User", on_delete=models.DO_NOTHING) # 上一个借阅者


class Login_record(models.Model):
    """用户登录记录表"""
    id = models.AutoField(primary_key=True) # 这条记录的 id
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING) # 登陆的用户的 id
    login_time = models.DateTimeField(null=False) # 用户登录的时间


class Request(models.Model):
    id = models.AutoField(primary_key=True) # 这条记录的 id，也就是这条借阅请求的 id
    book_name = models.ForeignKey("Book_list", on_delete=models.DO_NOTHING) # 请求借阅的书的 id
    cretime = models.DateTimeField(null=False) # 请求创建时间
    requster = models.ForeignKey("User", on_delete=models.DO_NOTHING) # 请求者
    confirm_code = models.SmallIntegerField(default=0, null=False) # 请求状态码
    expiry_time = models.DateTimeField(null=False) # 请求失效时间


class User(models.Model):
    """用户信息表"""
    id = models.AutoField(primary_key=True) # 这条记录的 id，也是用户的 id，区分用户的第二选择
    stu_id = models.CharField(max_length=12, null=False) # 用户学号，区分用户的第一选择
    user_name = models.CharField(max_length=10, null=False) # 用户的用户名
    password = models.CharField(max_length=16, null=False) # 用户密码
    email = models.CharField(max_length=30, null=False) # 用户邮箱
    phone = models.CharField(max_length=14, null=False) # 用户电话
    holds = models.IntegerField(default=0, null=True) # 用户目前借了几本书
    cretime = models.DateTimeField(null=False) # 账户建立时间
    last_time = models.DateTimeField(null=True) # 账户最后登录时间
    cancellation = models.BooleanField(default=0, null=False) # 账户是否已注销


class Book_short_comment(models.Model):
    """书籍简评表"""
    id = models.AutoField(primary_key=True) # 这条记录的 id，也是每条简评的 id
    book = models.ForeignKey("Book_list", on_delete=models.DO_NOTHING) # 书籍 id
    commentator = models.ForeignKey("User", on_delete=models.DO_NOTHING) # 评论用户的 id
    comment_text = models.TextField(max_length=300, null=False) # 评论正文
    comment_time = models.DateTimeField(null=False) # 评论创建时间
    like_num = models.IntegerField(default=0) # 喜欢数
    unlike_num = models.IntegerField(default=0) # 不喜欢数
    collect_num = models.IntegerField(default=0) # 收藏数


class Book_short_comment_like_and_collection_record(models.Model):
    """书籍简评的点赞和收藏记录表"""
    id = models.AutoField(primary_key=True) # 这条记录的 id，也是每条点赞收藏的 id
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING) # 记录归属的用户 id
    comment = models.ForeignKey("Book_short_comment", on_delete=models.DO_NOTHING) # 评论 id
    like_state = models.BooleanField(default=0, null=False) # 该用户是否喜欢这条简评
    unlike_state = models.BooleanField(default=0, null=False) # 该用户是否不喜欢这条简评
    collection_state = models.BooleanField(default=0, null=False) # 该用户是否收藏了这条简评

