import json
import re
from course2.ulities import check_role_edu, check_role_s, check_role_t
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from account.form import LoginForm, ChangePwdForm
from account.models import User


def login_(request):
    if request.method == "GET":
        obj = LoginForm()
        return render(request, "login.html", {"obj": obj})
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = LoginForm(request.POST)
        if obj.is_valid():
            username = obj.cleaned_data.get("username")
            password = obj.cleaned_data.get("password")
            # print(password)
            user = authenticate(request, username=username, password=password)

            # 教务
            if user:
                login(request, user)
                if user.is_first_login:
                    ret["msg"] = 0
                    return HttpResponse(json.dumps(ret, ensure_ascii=False))
                else:
                    if user.role_id == 1:
                        ret["msg"] = 1
                    # 教师
                    elif user.role_id == 2:
                        ret["msg"] = 2
                    # 学生
                    elif user.role_id == 3:
                        ret["msg"] = 3
                    return HttpResponse(json.dumps(ret, ensure_ascii=False))
            else:
                ret["status"] = False
                ret["msg"] = "用户名或密码错误，请核对后重新输入"
                return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = "用户名输入格式有误，请重新输入"
            print(ret["msg"])
            return HttpResponse(json.dumps(ret, ensure_ascii=False))



@login_required
def logout_(request):
    logout(request)
    return redirect("login.html")


@user_passes_test(check_role_edu)
@login_required
def reset_password(request):
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        no = request.POST.get("no")

        try:
            user = User.objects.get(username=no)
            user.set_password(user.card_id[-6:])
            user.save()
            return HttpResponse(json.dumps(ret, ensure_ascii=False))

        except Exception as e:
            print(str(e))
            ret["status"] = False
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
@user_passes_test(check_role_s)
def s_information(request):
    return render(request, "s_info.html")


@login_required
@user_passes_test(check_role_t)
def t_information(request):
    return render(request, "t_info.html")


@login_required
@user_passes_test(check_role_edu)
def e_information(request):
    return render(request, "e_info.html")


@login_required
def edit_information(request):
    if request.method == "POST":
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        qq = request.POST.get("qq")
        print(email, telephone, qq)
        error_dic = {}
        ret = {"status": True, "msg": error_dic}
        if email:
            if re.match(r'^\w+?@\w+?\.\w+?$', email):
                request.user.email = email
                request.user.save()
            else:
                ret["status"] = False
                error_dic.update({"email": "输入格式错误"})
        if telephone:
            if re.match(r'^\d{11}$', telephone):
                request.user.email = email
                request.user.save()
            else:
                ret["status"] = False
                error_dic.update({"telephone": "输入格式错误"})
        if qq:
            if re.match(r'^\d{6,10}$', qq):
                request.user.QQ = qq
                request.user.save()
            else:
                ret["status"] = False
                error_dic.update({"qq": "输出格式错误"})
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
def change_pwd(request):
    if request.method == "GET":
        obj = ChangePwdForm()
        return render(request, "change_password.html", {"obj": obj})
    if request.method == "POST":
        ret = {"status": None, "msg": None}
        obj = ChangePwdForm(request.POST)
        if obj.is_valid():
            old_password = obj.cleaned_data.get("old_password")
            password1 = obj.cleaned_data.get("password1")
            password2 = obj.cleaned_data.get("password2")
            user = authenticate(request, username=request.user.username, password=old_password)
            if not user:
                ret["status"] = "old_failed"
                ret["msg"] = "旧密码输入错误，请重新输入"
                return HttpResponse(json.dumps(ret, ensure_ascii=False))

            else:
                if password1 == old_password:
                    ret["status"] = "not_ok"
                    ret["msg"] = "新密码不能与旧密码相同"
                else:
                    if password1 == password2:
                        ret["status"] = "success"
                        user.set_password(password1)
                        user.is_first_login = False
                        user.save()
                        return HttpResponse(json.dumps(ret, ensure_ascii=False))
                    else:
                        ret["status"] = "diff_failed"
                        ret["msg"] = "两次密码输入不一致，请重新输入"
                        return HttpResponse(json.dumps(ret, ensure_ascii=False))

        else:
            ret["status"] = "form_failed"
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


@login_required
def change_avatar(request):
    if request.method == "POST":
        avatar = request.FILES.get("avatar")
        request.user.avatar = avatar
        request.user.save()
        if request.user.role_id == 1:
            return redirect('e_information.html')
        if request.user.role_id == 2:
            return redirect('t_information.html')
        if request.user.role_id == 3:
            return redirect('s_information.html')
