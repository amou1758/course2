import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
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
            user = authenticate(username=request.user, password=old_password)
            if user is None:
                ret["status"] = "old_failed"
                ret["msg"] = "旧密码输入错误，请重新输入"
                return HttpResponse(json.dumps(ret, ensure_ascii=False))

            else:
                if password1 == old_password:
                    ret["status"] = "not_ok"
                    ret["msg"] = "新密码不与旧密码相同"
                else:
                    if password1 == password2:
                        ret["status"] = "success"
                        # 这种改法 直接明文写入数据库 不对 也不好
                        # User.objects.filter(username=request.user).update(password=password1)
                        user.set_password(password1)
                        user.save()
                        PwdStatus.objects.filter(user__username=user).update(pwd_status=True)

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
def logout_(request):
    logout(request)
    return redirect("login.html")


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
