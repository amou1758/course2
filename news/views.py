import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.models import User
from news.form import NewsForm
from news.models import News


def new_news(request):
    if request.method == "GET":
        obj = NewsForm()
        return render(request, "e_newNews.html", {"obj": obj})
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = NewsForm(request.POST)
        if obj.is_valid():
            try:
                News.objects.create(
                    title=obj.cleaned_data.get("title"),
                    content=obj.cleaned_data.get("content"),
                    watcher=obj.cleaned_data.get("watcher"),
                    created_by=request.user,
                    modify_by=request.user
                )

                ret["msg"] = "发布成功"
            except Exception as e:
                print(e)
                ret["msg"] = "数据库写入异常，请联系管理员，错误代码:" + str(e)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret["status"] = False
            ret["msg"] = obj.errors
            print('新闻发布格式出错', ret['msg'])
            return HttpResponse(json.dumps(ret, ensure_ascii=False))


def m_news_detail(request):
    nid = request.GET.get("nid")
    data = []
    news = News.objects.filter(id=nid)
    for n in news:
        data.extend([n.title, n.content, n.ctime.strftime("%Y/%m/%d %H:%M"), n.created_by.name,
                     n.mtime.strftime("%Y/%m/%d %H:%M"), n.modify_by.name, n.watcher])
        print(n.ctime.strftime("%H:%M"))
    return HttpResponse(json.dumps(data, ensure_ascii=False))


def mod_news(request, nid):
    if request.method == "GET":
        news = News.objects.get(id=nid)
        obj = NewsForm({
            'nid': nid,
            'title': news.title,
            'content': news.content,
            'watcher': news.watcher
        })
        return render(request, "e_m_news.html", locals())
    if request.method == "POST":
        ret = {"status": True, "msg": None}
        obj = NewsForm(request.POST)
        if obj.is_valid():

            News.objects.filter(id=nid).update(
                title=obj.cleaned_data.get("title"),
                content=obj.cleaned_data.get("content"),
                watcher=obj.cleaned_data.get("watcher"),
                modify_by=request.user,
                mtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            )
            try:
                ret["msg"] = "修改成功"
            except Exception as e:
                print(e)
                ret["msg"] = "数据库写入异常，请联系管理员，错误代码:" + str(e)
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:

            ret["status"] = False
            ret["msg"] = obj.errors
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
