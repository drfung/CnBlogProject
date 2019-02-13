from django import forms
from django.forms import widgets
from .models import UserInfo
from django.core.exceptions import ValidationError,NON_FIELD_ERRORS


class UserForm(forms.Form):
    user = forms.CharField(max_length=32, label="用户名", widget=widgets.TextInput(attrs={"class": "form-control"}),
                           error_messages={"required": "该字段不能为空"}, )
    pwd = forms.CharField(max_length=32, label="密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                          error_messages={"required": "该字段不能为空"}, )
    re_pwd = forms.CharField(max_length=32, label="确认密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                             error_messages={"required": "该字段不能为空"}, )
    email = forms.EmailField(max_length=32, label="邮箱", widget=widgets.TextInput(attrs={"class": "form-control"}),
                             error_messages={"required": "该字段不能为空"}, )

    def clean_user(self):
        val = self.cleaned_data.get("user")
        user = UserInfo.objects.filter(username=val)
        if not user:
            return val
        else:
            raise ValidationError("该用户已注册")

    def  clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")

        if pwd and re_pwd:
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次输入密码不一致")
        else:
            return self.cleaned_data
