import datetime

from django.core.validators import RegexValidator
from django.forms import fields, widgets
from django import forms

from course.models import Course


class PubForm(forms.ModelForm):
    course_no = fields.CharField(

        required=True,
        label="课程号",
        validators=[RegexValidator(regex='^[0-9]{10}$', message="请输入数字")],
        error_messages={
            'required': '该字段必须要输入',
            'invalid': '课程号为8位数字'
        }
    )
    course_name = fields.CharField(
        max_length=30,
        min_length=2,
        required=True,
        label="课程名",
        error_messages={
            'max_length': '最大不能超过30个字',
            'min_length': '最小不能少于2个字',
            'invalid': '不符合格式要求'
        }
    )

    course_credit = fields.DecimalField(max_digits=2, decimal_places=1, max_value=5.0,
                                        error_messages={
                                            'invalid': '必须为一位小数',
                                            'max_value': '最大学分不应该超过5.0'
                                        },
                                        label="学分"

                                        )
    course_desc = fields.CharField(
        widget=widgets.Textarea(),
        max_length=140,
        initial="暂无",
        label="课程描述"
    )

    class Meta:
        model = Course
        fields = ["course_college", ]

    # 解决form初始化时数据库数据不刷新问题
    def __init__(self, *args, **kwargs):
        super(PubForm, self).__init__(*args, **kwargs)
        cour = Course.objects.last().course_no
        c_date = cour[:8]
        n_date = datetime.datetime.now().strftime("%Y%m%d")
        if n_date > c_date:
            ini_no = n_date + '01'
        else:
            ini_no = str(int(cour) + 1)
        self.fields['course_no'].initial = ini_no


class AppForm(forms.ModelForm):
    course_total_people = fields.IntegerField(
        initial=30,
        min_value=10,
        max_value=200,
        required=True,
        validators=[RegexValidator(r'^\d{2,3}$', "输入整数")],
        error_messages={
            "invalid": "课程名额必须在10-200之间",
            # "required":"该字段必须要输入整数值"
        }
    )

    class Meta:
        model = Course
        fields = ["course_week", "course_time", "course_classroom", "course_total_people", "course_type"]


class ExtendForm(forms.Form):
    people = forms.IntegerField(
        widget=widgets.NumberInput(),
        initial=0,
        min_value=0,
        max_value=100,
        required=True,
        validators=[RegexValidator(r'^\d{1,3}$', "输入正整数")],
        error_messages={
            "invalid": "课程名额扩容应该在1-100之间",
        }
    )

    days = forms.ChoiceField(
        choices=((0, 0), (1, 1), (2, 2), (3, 3,), (4, 4), (5, 5), (6, 6), (7, 7))
    )


class CourseSearchForm(forms.Form):
    content = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入课程号或课程名"}),
        max_length=30
    )


class NewsSearchForm(forms.Form):
    content = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={"class": "form-control", "placeholder": "请输入标题"}),
        max_length=30
    )
