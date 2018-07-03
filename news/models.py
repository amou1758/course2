from django.db import models
from account.models import User


# Create your models here.
from extra_app.DjangoUeditor.models import UEditorField


class News(models.Model):
    title = models.CharField(max_length=40)
    content = UEditorField(max_length=6000, width=1000, height=300, toolbars='normal', imagePath='news_images/',
                           filePath='news_files/', upload_settings={'imageMaxSize': 120400000},
                           settings={}, command=None, verbose_name="正文")
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='空缺')
    modify_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modify_news')
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    watcher = models.IntegerField(choices=((1, '所有人'),
                                           (2, '仅老师'),
                                           (3, '仅学生'),))

    def __str__(self):
        return self.title
