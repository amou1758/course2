import datetime
import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from course.form import PubForm, AppForm
from course2.ulities import MyPagination
from news.models import News
from .models import Course
# Create your views here.


def e_index(request):
    app_list = Course.objects.filter(course_status=1).order_by('course_applied_time')
    app_counts = app_list.count()
    news = News.objects.all()
    return render(request, 'e_index.html', locals())


def e_news(request):
    news_list = News.objects.all().order_by("-ctime")
    return render(request, "e_news.html", {"news_list": news_list})


def pub_course(request):
    if request.method == "GET":
        courses = Course.objects.all().order_by('-course_ctime')
        pub_form = PubForm()
        obj = MyPagination(courses.count(), request.GET.get('p'), 10, url='e_pubCourse.html')
        courses = courses[obj.start():obj.end()]
        return render(request, "e_pubCourse.html", {"pub_form": pub_form, "courses": courses, "obj": obj})
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        pub_form = PubForm(request.POST)
        if pub_form.is_valid():
            try:
                Course.objects.create(
                    course_no=pub_form.cleaned_data.get("course_no"),
                    course_name=pub_form.cleaned_data.get("course_name"),
                    course_credit=pub_form.cleaned_data.get("course_credit"),
                    course_desc=pub_form.cleaned_data.get("course_desc"),
                    course_college=pub_form.cleaned_data.get("course_college"),
                    course_starter=request.user,
                )
                ret["msg"] = "发布成功"

            except Exception as e:
                ret["status"] = False
                if str(e) == "UNIQUE constraint failed: course_course.course_no":
                    ret["msg"] = "课程号已经被使用，请重写填写"
                else:
                    ret["msg"] = "数据库写入异常，请联系管理员，错误代码:" + str(e)
            return HttpResponse(json.dumps(ret))
        else:
            ret["status"] = False
            ret["msg"] = pub_form.errors
            return HttpResponse(json.dumps(ret))


def t_index(request):
    today_ = datetime.datetime.now().weekday() + 1
    today_courses = Course.objects.filter(course_choosed=True, course_teacher=request.user, course_week=today_)
    news = News.objects.filter(Q(watcher=1) | Q(watcher=2)).order_by("-mtime")
    return render(request, "t_index.html", {"today_course": today_courses, "news": news})


def t_apply(request):
    if request.method == "GET":
        obj = AppForm()
        courses = Course.objects.filter(course_status=0).order_by('-course_ctime')
        obj2 = MyPagination(courses.count(), request.GET.get('p'), 10, url='t_apply.html')
        courses = courses[obj2.start():obj2.end()]
        return render(request, "t_apply.html", {"courses": courses, "obj": obj, "obj2": obj2})
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = AppForm(request.POST)
        print(obj)
        if obj.is_valid():
            try:
                Course.objects.filter(course_no=request.POST.get("cno")).update(
                    course_teacher=request.user,
                    course_applied_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    course_week=obj.cleaned_data.get("course_week"),
                    course_time=obj.cleaned_data.get("course_time"),
                    course_classroom=obj.cleaned_data.get("course_classroom"),
                    course_total_people=obj.cleaned_data.get("course_total_people"),
                    course_type=obj.cleaned_data.get("course_type"),
                    course_status=1
                )

                ret["msg"] = "申请成功"
            except Exception as e:
                print(str(e))
                if str(
                        e) == "UNIQUE constraint failed: course_course.course_teacher_id, course_course.course_week, course_course.course_time":
                    ret["status"] = False
                    ret["msg"] = "该教室已被使用，请另选择时间段或教室"
                    return HttpResponse(json.dumps(ret, ensure_ascii=False))
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


def t_applied(request):
    applied_course_list = Course.objects.filter(course_teacher=request.user).order_by("-course_applied_time")
    return render(request, "t_applied.html", {"applied_course_list": applied_course_list})


def t_online(request):
    if request.method == "POST":
        ret = {"status": True}
        n = datetime.datetime.now()
        d = datetime.timedelta(days=3)
        cno = request.POST.get("cno")
        Course.objects.filter(course_no=cno).update(
            course_online=True,
            course_online_time=n,
            course_status=4,
            course_close_time=(n + d).strftime("%Y-%m-%d %H:%M"),
        )
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


def t_extend(request):
    if request.method == "POST":
        cno = request.POST.get("cno")
        days = request.POST.get("days")
        ntime = datetime.datetime.now()
        cour = Course.objects.get(course_no=cno)
        if ntime < cour.course_close_time:
            cour.course_close_time += datetime.timedelta(days=days)


def e_aprrove(request):
    app_list = Course.objects.filter(course_status=1)
    return render(request, "e_approve.html", {"app_list": app_list})


def pass_(request):
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        cno = request.POST.get("cno")
        Course.objects.filter(course_no=cno).update(
            course_status=2,
            course_approver=request.user
        )

        ret["msg"] = "该课程通过审批"
        return HttpResponse(json.dumps(ret))


def no_pass(request):
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        cno = request.POST.get("cno")
        Course.objects.filter(course_no=cno).update(
            course_status=3,
            course_approver=request.user
        )
        ret["msg"] = "该课程未通过审批"
        return HttpResponse(json.dumps(ret))
