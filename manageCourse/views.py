import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render
from course2.ulities import check_role_edu
# Create your views here.
from account.models import User, Grade
from course.form import CourseSearchForm, NewsSearchForm, PeopleSearchForm, AddTeacher, AddStudent
from course.models import Course
from course2.ulities import MyPagination
from news.models import News
from django.core.exceptions import ValidationError

@user_passes_test(check_role_edu)
@login_required
def m_course(request):
    if request.method == "GET":
        courses = Course.objects.all()
        fm = CourseSearchForm()
        obj = MyPagination(courses.count(), request.GET.get('p'), 10, url="m_course")
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


@user_passes_test(check_role_edu)
@login_required
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
@login_required
@user_passes_test(check_role_edu)
def m_course_del(request):
    if request.method == "POST":
        ret = {"status": True, "msg": "删除成功！"}
        ls = request.POST.getlist("cno[]")
        for i in ls:
            Course.objects.filter(course_no=i).delete()
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
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


@login_required
@user_passes_test(check_role_edu)
def m_news_del(request):
    if request.method == "POST":
        ret = {"status": True, "msg": "删除成功！"}
        ls = request.POST.getlist("nid[]")
        for i in ls:
            News.objects.filter(id=i).delete()
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
def m_teacher(request):
    if request.method == "GET":
        fm = PeopleSearchForm()
        t = User.objects.filter(role=2)
        obj = MyPagination(t.count(), request.GET.get("p"), 10, url='m_teacher')
        teachers = t[obj.start():obj.end()]
        return render(request, "m_teacher.html", {"teachers": teachers, "obj": obj, "fm": fm})
    if request.method == "POST":
        fm = PeopleSearchForm(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            if content.isdigit():
                t = User.objects.filter(username__contains=content, role=2)
            else:
                t = User.objects.filter(name__contains=content, role=2)
            obj = MyPagination(t.count(), request.GET.get("p"), 10, url='m_teacher')
            teachers = t[obj.start():obj.end()]
            return render(request, 'm_teacher.html', {"teachers": teachers, "fm": fm, "obj": obj})
        else:
            return HttpResponse("输入不符合要求，请重新输入")


@login_required
@user_passes_test(check_role_edu)
def m_teacher_detail(request):
    no = request.GET.get("no")
    data = []

    teacher = User.objects.get(username=no)
    data.extend([teacher.name, teacher.username, teacher.get_gender_display(), teacher.get_college_display(),
                 teacher.get_place_display(), teacher.get_province_display(), teacher.card_id,
                 teacher.get_nation_display(),
                 teacher.email, teacher.telephone, teacher.birthday.strftime("%Y-%m-%d"), teacher.QQ
                 ])

    return HttpResponse(json.dumps(data, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
def m_edit_teacher(request):
    if request.method == "GET":
        no = request.GET.get("no")
        print(no)
        data = []
        teacher = User.objects.get(username=no)
        data.extend([
            teacher.name, teacher.username, teacher.gender, teacher.college,
            teacher.place, teacher.province, teacher.card_id, teacher.nation,
            teacher.email, teacher.telephone, teacher.QQ
        ])
        print(data)
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = AddTeacher(request.POST)
        print(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get("username")
            name = obj.cleaned_data.get("name")
            gender = obj.cleaned_data.get("gender")
            college = obj.cleaned_data.get("college")
            place = obj.cleaned_data.get("place")
            province = obj.cleaned_data.get("province")
            card_id = obj.cleaned_data.get("card_id")
            nation = obj.cleaned_data.get("nation")
            email = obj.cleaned_data.get("email")
            telephone = obj.cleaned_data.get("telephone")
            qq = obj.cleaned_data.get("qq")
            # print(username,name)
            User.objects.filter(username=username).update(
                name=name,
                gender=gender,
                college=college,
                place=place,
                province=province,
                card_id=card_id,
                nation=nation,
                email=email,
                telephone=telephone,
                QQ=qq,

            )
            ret["msg"] = "创建成功"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            print(obj.errors)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
def m_add_teacher(request):
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = AddTeacher(request.POST)

        if obj.is_valid():
            username = obj.cleaned_data.get("username")
            name = obj.cleaned_data.get("name")
            gender = obj.cleaned_data.get("gender")
            college = obj.cleaned_data.get("college")
            place = obj.cleaned_data.get("place")
            province = obj.cleaned_data.get("province")
            card_id = obj.cleaned_data.get("card_id")
            nation = obj.cleaned_data.get("nation")
            email = obj.cleaned_data.get("email")
            telephone = obj.cleaned_data.get("telephone")
            qq = obj.cleaned_data.get("qq")
            print(obj.cleaned_data)
            try:
                user = User(
                username=username,
                name=name,
                gender=gender,
                college=college,
                place=place,
                province=province,
                card_id=card_id,
                nation=nation,
                email=email,
                telephone=telephone,
                QQ=qq,
                birthday=card_id[6:10] + '-' + card_id[10:12] + '-' + card_id[12:14],
                role_id=2
                )
                user.set_password(card_id[-6:])
                user.save()
                ret["msg"] = "创建成功"
                return HttpResponse(json.dumps(ret, ensure_ascii=False))
            except ValidationError as e:
                print(str(e))
                ret["msg"] = str(e)
                ret["status"] = False
                return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            print(obj.errors)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
def m_student(request):
    if request.method == "GET":
        fm = PeopleSearchForm()
        s = User.objects.filter(role=3)
        obj = MyPagination(s.count(), request.GET.get("p"), 10, url='m_student')
        students = s[obj.start():obj.end()]
        return render(request, "m_student.html", {"students": students, "obj": obj, "fm": fm})
    if request.method == "POST":
        fm = PeopleSearchForm(request.POST)
        if fm.is_valid():
            content = fm.cleaned_data.get("content")
            if content.isdigit():
                s = User.objects.filter(username__contains=content, role=3)
            else:
                s = User.objects.filter(name__contains=content, role=3)
            obj = MyPagination(s.count(), request.GET.get("p"), 10, url='m_student')
            students = s[obj.start():obj.end()]
            return render(request, 'm_student.html', {"students": students, "fm": fm, "obj": obj})
        else:
            return HttpResponse("输入不符合要求，请重新输入")


@login_required
@user_passes_test(check_role_edu)
def m_student_detail(request):
    no = request.GET.get("no")
    data = []

    student = User.objects.get(username=no)
    data.extend([student.name, student.username, student.get_gender_display(), student.get_college_display(),
                 student.grade.name, student.get_province_display(), student.card_id, student.get_nation_display(),
                 student.email, student.telephone, student.birthday.strftime("%Y-%m-%d"), student.QQ
                 ])
    return HttpResponse(json.dumps(data, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
def m_edit_student(request):
    if request.method == "GET":
        no = request.GET.get("no")
        print(no)
        data = []
        student = User.objects.get(username=no)
        data.extend([
            student.name, student.username, student.gender, student.college,
            student.grade.id, student.province, student.card_id, student.nation,
            student.email, student.telephone, student.QQ
        ])
        print(data)
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = AddStudent(request.POST)
        print(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get("username")
            name = obj.cleaned_data.get("name")
            gender = obj.cleaned_data.get("gender")
            college = obj.cleaned_data.get("college")
            grade = obj.cleaned_data.get("grade")
            province = obj.cleaned_data.get("province")
            card_id = obj.cleaned_data.get("card_id")
            nation = obj.cleaned_data.get("nation")
            email = obj.cleaned_data.get("email")
            telephone = obj.cleaned_data.get("telephone")
            qq = obj.cleaned_data.get("qq")
            # print(username,name)
            User.objects.filter(username=username).update(
                name=name,
                gender=gender,
                college=college,
                grade=grade,
                province=province,
                card_id=card_id,
                nation=nation,
                email=email,
                telephone=telephone,
                QQ=qq,
            )
            ret["msg"] = "创建成功"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            print(obj.errors)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
def m_add_student(request):
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = AddStudent(request.POST)

        if obj.is_valid():
            username = obj.cleaned_data.get("username")
            name = obj.cleaned_data.get("name")
            gender = obj.cleaned_data.get("gender")
            college = obj.cleaned_data.get("college")
            grade = obj.cleaned_data.get("grade")
            province = obj.cleaned_data.get("province")
            card_id = obj.cleaned_data.get("card_id")
            nation = obj.cleaned_data.get("nation")
            email = obj.cleaned_data.get("email")
            telephone = obj.cleaned_data.get("telephone")
            qq = obj.cleaned_data.get("qq")
            print(obj.cleaned_data)
            grade_ = Grade.objects.get(id=grade)
            try:
                user = User(
                    username=username,
                    name=name,
                    gender=gender,
                    college=college,
                    grade=grade_,
                    province=province,
                    card_id=card_id,
                    nation=nation,
                    email=email,
                    telephone=telephone,
                    QQ=qq,
                    birthday=card_id[6:10] + '-' + card_id[10:12] + '-' + card_id[12:14],
                    role_id=3
                )
                user.set_password(card_id[-6:])
                user.save()
                ret["msg"] = "创建成功"
                return HttpResponse(json.dumps(ret, ensure_ascii=False))
            except ValidationError as e:
                print(str(e))
                ret["msg"] = str(e)
                ret["status"] = False
                return HttpResponse(json.dumps(ret, ensure_ascii=False))


        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            print(obj.errors)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_role_edu)
def m_del_student(request):
    if request.method == "POST":
        ret = {"status": True, "msg": "删除成功"}
        try:
            ls = request.POST.getlist("no[]")
            for i in ls:
                User.objects.filter(username=i).delete()
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        except Exception as e:
            print(str(e))
            ret["status"] = False
            ret["msg"] = "删除失败"
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
