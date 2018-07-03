from django import forms
from django.forms import fields, widgets

from news.models import News


class NewsForm(forms.ModelForm):
    title = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "在此输入标题"})
    )

    choices = ((1, '所有人'),
               (2, '仅老师'),
               (3, '仅学生'),)
    watcher = fields.CharField(
        widget=widgets.Select(choices=choices),
        label="可见对象",

    )

    class Meta:
        model = News
        fields = ["title", "content", "watcher"]
