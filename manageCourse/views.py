import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from course.form import CourseSearchForm, NewsSearchForm
from course.models import Course
from course2.ulities import MyPagination
from news.models import News


def m_course(request):
    if request.method == "GET":
        courses = Course.objects.all()
        fm = CourseSearchForm()
        obj = MyPagination(courses.count(), request.GET.get('p'), 13, url="m_course")
        courses = courses[obj.start():obj.end()]

        return render(request, "m_course.html", {"courses": courses, "obj": obj, "fm": fm})
    if request.method == "POST":
        fm = CourseSearchForm(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            if content.isdigit():
                courses = Course.objects.filter(course_no__contains=content).order_by("-course_ctime")

            else:
                courses = Course.objects.filter(course_name__contains=content).order_by("-course_ctime")
            obj = MyPagination(courses.count(), request.GET.get("p"), 10, url='m_course')
            courses = courses[obj.start():obj.end()]
            return render(request, 'm_course.html', {"courses": courses, "fm": fm, "obj": obj})
        else:
            return HttpResponse("输入不符合要求，请重新输入")


def m_course_detail(request):
    cno = request.GET.get("cno")
    data = []
    course = Course.objects.get(course_no=cno)
    print(cno)
    teacher = course.course_teacher
    if not teacher:
        teacher = '——'
    else:
        teacher = teacher.name
    if not course.course_type:
        course.course_type = '——'
    classroom = course.get_course_classroom_display()
    if not course.course_classroom:
        classroom = '——'
    week = course.get_course_week_display()
    if not course.course_week:
        week = '——'
    time_ = course.get_course_time_display()
    if not course.course_time:
        time_ = '——'
    week_time = week + ' ' + time_
    approver = course.course_approver
    if not approver:
        approver = '——'
    else:
        approver = approver.name
    if not course.course_total_people:
        course.course_total_people = '——'
    type_ = course.course_type
    if not type_:
        type_ = '——'
    else:
        type_ = course.get_course_type_display()
    # 课程详情包括
    data.extend([course.course_no, course.course_name, course.course_ctime.strftime("%Y-%m-%d %H:%M"),
                 float(course.course_credit), course.course_desc, course.course_starter.name,
                 course.get_course_college_display(), teacher,
                 type_, classroom,
                 week_time,
                 approver, course.course_total_people, course.course_choosed_student
                 ])
    print(data)
    return HttpResponse(json.dumps(data, ensure_ascii=False))


# def m_offline(request):
#     if request.method == "POST":
#         ret = {"status": True, "msg": "下线成功"}
#         try:
#             ls = request.POST.getlist("cno[]")
#             print(ls)
#             for i in ls:
#                 Course.objects.filter(course_no=i).update(#)
#             return HttpResponse(json.dumps(ret, ensure_ascii=False))
#         except Exception as e:
#             print(str(e))
#             ret["status"] = False
#             ret["msg"] = "下线失败"
#             return HttpResponse(json.dumps(ret, ensure_ascii=False))
#
# def m_online(request):
#     if request.method == "POST":
#         ret = {"status": True, "msg": "上线成功"}
#         try:
#             ls = request.POST.getlist("cno[]")
#             print(ls)
#             for i in ls:
#                 Course.objects.filter(course_no=i).update(#)
#             return HttpResponse(json.dumps(ret, ensure_ascii=False))
#         except Exception as e:
#             print(str(e))
#             ret["status"] = False
#             ret["msg"] = "上线失败"
#             return HttpResponse(json.dumps(ret, ensure_ascii=False))

def m_course_del(request):
    if request.method == "POST":
        ret = {"status": True, "msg": "删除成功！"}
        ls = request.POST.getlist("cno[]")
        for i in ls:
            Course.objects.filter(course_no=i).delete()
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


def m_news(request):
    if request.method == "GET":
        fm = CourseSearchForm()
        news = News.objects.all().order_by("-ctime")
        obj = MyPagination(news.count(), request.GET.get("p"), 10, url='m_news')
        news = news[obj.start():obj.end()]
        return render(request, "m_news.html", locals())
    if request.method == "POST":
        fm = NewsSearchForm(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            news = News.objects.filter(title__contains=content).order_by("-ctime")
            obj = MyPagination(news.count(), request.GET.get("p"), 10, url='m_news')
            news = news[obj.start():obj.end()]
            return render(request, 'm_news.html', {"news": news, "fm": fm})
        else:
            return HttpResponse("输入不符合要求，请重新输入")


def m_news_del(request):
    if request.method == "POST":
        ret = {"status": True, "msg": "删除成功！"}
        ls = request.POST.getlist("nid[]")
        for i in ls:
            News.objects.filter(id=i).delete()
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
