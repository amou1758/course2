from django.contrib import admin
from account.models import User
from news.models import News
from course.models import Course
# Register your models here.

admin.site.register(User)
admin.site.register(News)
admin.site.register(Course)
