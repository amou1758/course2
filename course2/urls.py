"""course2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from extra_app.DjangoUeditor import urls as DjangoUeditor_urls
from course import views
from course2 import settings
from news import views as news_views

urlpatterns = [
    path('admin/', admin.site.urls),
                  path('ueditor/', include(DjangoUeditor_urls)),

                  path('e/index.html', views.e_index),
                  path('e/news.html', views.e_news),
                  path('e/newNews.html', news_views.new_news, name='newNews'),
                  path('m_news_detail', news_views.m_news_detail),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
