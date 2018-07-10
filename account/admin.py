from django.contrib import admin
from account.models import User
from account.user_admin import CustomUserAdmin
from news.models import News
from course.models import Course
# Register your models here.

# admin.site.register(User, UserAdmin)
admin.site.register(News)
admin.site.register(Course)
admin.site.register(User, CustomUserAdmin)
