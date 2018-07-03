import json

from django.http import HttpResponse
from django.shortcuts import render

from news.models import News
from .models import Course
# Create your views here.


def e_index(request):
    app_list = Course.objects.filter(course_status=1).order_by('course_applied_time')
    app_counts = app_list.count()
    news = News.objects.all().order_by('-mtime', '-ctime')
    return render(request, 'e_index.html', locals())


def e_news(request):
    news_list = News.objects.all().order_by("-ctime")
    return render(request, "e_news.html", {"news_list": news_list})
