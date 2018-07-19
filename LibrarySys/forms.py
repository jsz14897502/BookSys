# encoding: utf-8

from django import forms


class LoginForm(forms.Form):
    pass


class SignupForm(forms.Form):
    stu_id = forms.CharField(max_length=12, min_length=12, label="学号")
    user_name = forms.CharField(max_length=10, min_length=2, label="用户名")
    password = forms.CharField(max_length=16, min_length=6, label="密码")
    password_confirm = forms.CharField(max_length=16, min_length=6, label="确认密码")
    email = forms.EmailField(label="邮箱")
    phone = forms.CharField(max_length=14, min_length=11, label="手机")



