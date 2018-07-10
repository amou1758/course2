from django.core.validators import RegexValidator
from django.forms import fields, widgets
from django import forms


class LoginForm(forms.Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "学号/工号"}),
        label="ID",
        validators=[RegexValidator(r'^\d{8,11}$')],
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '输入不符合要求'
        }
    )

    password = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "password", "class": "form-control", "placeholder": "在这里输入密码"}),
        label="密码",
        help_text="初始密码为身份证后6位"
    )


class ChangePwdForm(forms.Form):
    old_password = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "password", "class": "form-control", "placeholder": "在这里输入旧密码"}),
        label="旧密码",
        help_text="初始密码为身份证后6位",
        required=True,
        error_messages={
            'required': '该字段必须要输入'
        }
    )

    password1 = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "password", "class": "form-control", "placeholder": "在这里输入新密码"}),
        validators=[RegexValidator(r'^\w{8,18}$')],
        label="新密码",
        help_text="密码应含为字母或数字，且长度为8-18个字符",
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '输入密码不符合要求'
        }

    )

    password2 = fields.CharField(
        widget=widgets.TextInput(attrs={"type": "password", "class": "form-control", "placeholder": "再次输入新密码"}),
        label="确认新密码",
        help_text="密码应为有字母或数字，且长度不小于8个字符",
        validators=[RegexValidator(r'^\w{8,18}$')],
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '输入密码不符合要求'
        }
    )

