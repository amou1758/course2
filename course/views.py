import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from course.form import PubForm, AppForm, ExtendForm, CourseSearchForm, AddTeacher, AddStudent
from course2.ulities import MyPagination
from news.models import News
from .models import Course, StudentCourse


# Create your views here.

@login_required
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

        obj = MyPagination(courses.count(), request.GET.get('p'), 15, url='pubCourse.html')
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


def m_manage_center(request):
    tfm = AddTeacher()
    sfm = AddStudent()
    return render(request, "e_manage_center.html", locals())


def t_index(request):
    today_ = datetime.datetime.now().weekday() + 1
    today_courses = Course.objects.filter(course_choosed_student__gte=1, course_teacher=request.user,
                                          course_week=today_)
    news = News.objects.filter(Q(watcher=1) | Q(watcher=2)).order_by("-mtime")
    return render(request, "t_index.html", {"today_course": today_courses, "news": news})

def t_apply(request):
    if request.method == "GET":
        obj = AppForm()
        courses = Course.objects.filter(course_status=0).order_by('-course_ctime')
        obj2 = MyPagination(courses.count(), request.GET.get('p'), 10, url='apply.html')
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
                    ret["msg"] = "该时段，你已经有其他课程了！"
                    return HttpResponse(json.dumps(ret, ensure_ascii=False))
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

def t_applied(request):
    applied_course_list = Course.objects.filter(course_teacher=request.user).order_by("-course_applied_time")
    extend_obj = ExtendForm()
    return render(request, "t_applied.html", {"applied_course_list": applied_course_list, "obj": extend_obj})

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

def t_offline(request):
    if request.method == "POST":
        n = datetime.datetime.now()
        ret = {"status": True}
        cno = request.POST.get("cno")
        Course.objects.filter(course_no=cno).update(
            course_online=False,
            course_status=5,
            course_close_time=n.strftime("%Y-%m-%d %H:%M"),
        )
        return HttpResponse(json.dumps(ret, ensure_ascii=False))

def t_extend(request):
    if request.method == "POST":
        obj = ExtendForm(request.POST)
        ret = {"status": True, "msg": None}
        if obj.is_valid():
            cno = request.POST.get("cno")
            people = obj.cleaned_data.get("people")
            days = obj.cleaned_data.get("days")
            print(cno, people, days)
            cour = Course.objects.get(course_no=cno)
            cour.course_total_people += people
            cour.course_close_time += datetime.timedelta(days=int(days))
            cour.save()
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            print(obj.errors)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


def t_student_list(request):
    pass

def t_table(request):
    courses = Course.objects.filter(course_teacher=request.user, course_choosed_student__gte=1)
    weeks = [i for i in range(1, 6)]
    return render(request, "t_table.html", {"courses": courses, "weeks": weeks})







def s_index(request):
    today_ = datetime.datetime.now().weekday() + 1
    today_courses = Course.objects.filter(studentcourse__student=request.user, studentcourse__is_choosed=True,
                                          course_week=today_).order_by("course_time")
    news = News.objects.filter(Q(watcher=1) | Q(watcher=3)).order_by("-mtime")
    obj = MyPagination(news.count(), request.GET.get("p"), 5, url='select.html')
    news = news[obj.start():obj.end()]
    return render(request, "s_index.html", {"obj": obj, "today_course": today_courses, "news": news})


def s_course_pool(request):
    if request.method == "GET":
        fm = CourseSearchForm()
        course_pool = Course.objects.filter(Q(course_online=True, course_college=request.user.college, \
                                              course_type=1) | Q(course_online=True, course_type=2)).exclude(
            studentcourse__student=request.user) \
            .order_by('-course_online_time')


        return render(request, "s_select.html", {"fm": fm, "course_pool": course_pool})

    if request.method == "POST":
        ret = {"status": True}
        cno = request.POST.get("cno")
        cour = Course.objects.get(course_no=cno)
        if cour.course_choosed_student < cour.course_total_people:
            cour.course_choosed_student += 1
            cour.save()
            StudentCourse.objects.create(
                student=request.user,
                course=cour
            )
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret = {"status": False}
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


def s_search_course(request):
    if request.method == "POST":
        fm = CourseSearchForm(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            if content.isdigit():
                course_ = Course.objects.filter(Q(course_online=True, course_college=request.user.college, \
                                                  course_type=1, course_no__contains=content) | Q(course_online=True,
                                                                                                  course_type=2,
                                                                                                  course_no__contains=content)).exclude(
                    studentcourse__student=request.user) \
                    .order_by('-course_online_time')
            else:
                course_ = Course.objects.filter(Q(course_online=True, course_college=request.user.college, \
                                                  course_type=1, course_name__contains=content) | Q(course_online=True,
                                                                                                    course_type=2,
                                                                                                    course_name__contains=content)).exclude(
                    studentcourse__student=request.user) \
                    .order_by('-course_online_time')

            obj = MyPagination(course_.count(), request.GET.get("p"), 10, url='select.html')
            course_pool = course_[obj.start():obj.end()]
            return render(request, 's_select.html', {"obj": obj, "fm": fm, "course_pool": course_pool})
        else:
            return HttpResponse("输入不符合要求，请重新输入")


def s_selected(request):
    selected_courses = Course.objects.filter(studentcourse__student=request.user,
                                             studentcourse__is_choosed=True
                                             )

    obj = MyPagination(selected_courses.count(), request.GET.get("p"), 10, url='select.html')
    selected_courses = selected_courses[obj.start():obj.end()]
    return render(request, "s_selected.html", {"obj": obj, "selected_courses": selected_courses})


def s_quit(request):
    if request.method == "POST":
        ret = {"status": True}
        cno = request.POST.get("cno")
        cour = Course.objects.get(course_no=cno)
        cour.course_choosed_student -= 1
        StudentCourse.objects.filter(course__course_no=cno).delete()
        cour.save()
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


def s_table(request):
    courses = Course.objects.filter(studentcourse__student=request.user, studentcourse__is_choosed=True)
    weeks = [i for i in range(1, 6)]
    return render(request, "s_table.html", {"courses": courses, "weeks": weeks})
