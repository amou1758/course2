from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
# 用户表

colleges = [
    (1, '新闻学院'),
    (2, '信息工程学院'),
    (3, '马克思研究学院'),
    (4, '医学院'),
    (5, '播音学院'),
    (6, '戏剧影视学院'),
    (7, '计算机学院'),
    (8, '外国语学院'),
]

provinces = [
    (1, '北京市'), (2, '天津市'), (3, '上海市'), (4, '重庆市'),
    (5, '河北省'), (6, '山西省'), (7, '辽宁省'), (8, '吉林省'),
    (9, '黑龙江省'), (10, '江苏省'), (11, '浙江省'), (12, '安徽省'),
    (13, '福建省'), (14, '江西省'), (15, '山东省'), (16, '河南省'),
    (17, '湖北省'), (18, '湖南省'), (19, '广东省'), (20, '海南省'),
    (21, '四川省'), (22, '贵州省'), (23, '云南省'), (24, '陕西省'),
    (25, '甘肃省'), (26, '青海省'), (27, '台湾省'), (28, '内蒙古自治区'),
    (29, '广西壮族自治区'), (30, '西藏自治区'), (31, '宁夏回族自治区'),
    (32, '新疆维吾尔自治区'), (33, '香港特别行政区'), (34, '澳门特别行政区')
]

nations = [
    (1, '汉族'), (2, '回族'), (3, '壮族'), (4, '蒙古族'), (5, '朝鲜族'), (6, '满族'),
    (7, '客家族'), (8, '维吾尔族'), (9, '藏族'), (10, '傣族'),
]


class Grade(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    userno = models.CharField(max_length=11, db_index=True, unique=True)
    username = models.CharField(max_length=32, db_index=True)
    is_first_login = models.BooleanField(default=True)
    gender = models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1)
    role = models.IntegerField(choices=[(1, '学生'), (2, '教师'), (3, '教务')])
    place = models.IntegerField(
        choices=[(1, '助教'), (2, '讲师'), (3, '高级讲师'), (4, '副教授'), (5, '教授'), (6, '高级教授'), (7, '特聘教授'), (8, '客座教授')],
        null=True)
    college = models.IntegerField(choices=colleges, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    card_id = models.CharField(max_length=18)
    nation = models.IntegerField(choices=nations)
    province = models.IntegerField(choices=provinces)
    email = models.EmailField()
    telephone = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='user_avatar', null=True, default=None)
    birthday = models.DateTimeField()
    qq = models.CharField(max_length=10)

    USERNAME_FIELD = 'userno'

    def __str__(self):
        return self.username
