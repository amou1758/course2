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
from django.urls import path, include, re_path
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
                  re_path(r'mod_news.html(?P<nid>\d+)', news_views.mod_news, name="mod_news"),

                  path('e/pubCourse.html', views.pub_course),
                  path('e/approve.html', views.e_aprrove),
                  path('e/pass', views.pass_, name="pass"),
                  path('e/noPass', views.no_pass, name="noPass"),

                  path('t/index.html', views.t_index),
                  path('t/apply.html', views.t_apply),
                  path('t/applied.html', views.t_applied),
                  path('t/online', views.t_online),
                  path('t/offline', views.t_offline),
                  path('t/extend', views.t_extend),
                  path('t/table.html', views.t_table),

                  path('s/index.html', views.s_index),
                  path('s/select.html', views.s_course_pool),
                  path('s/selected.html', views.s_selected),
                  path('s/search', views.s_search_course),
                  path('s/quit', views.s_quit),
                  path('s/table.html', views.s_table),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
