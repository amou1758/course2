from django.test import TestCase

# Create your tests here.


# 批量创建一些例子
from account.models import User
from news.models import News
import datetime
import random

ntime = datetime.datetime.now().strftime("%Y-%m-%d")
user = User.objects.get(username="88880001")
# 1 所有人 2 教师 3 学生
ran_choice = random.choices([1, 2, 3])
for i in range(10):
    News.objects.create(
        title="标题：" + str(i),
        content="内容乃是千篇一律，毫无新意",
        watcher=ran_choice[0],
        created_by=user,
        modify_by=user,
        mtime=ntime
    )
