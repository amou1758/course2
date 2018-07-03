from django.db import models
from account.models import User


# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField(max_length=3000)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='空缺')
    modify_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modify_news')
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    wathcer = models.CharField(choices=[('S', '学生'), ('T', '教师'), ('A', '所有人')])

    def __str__(self):
        return self.title
