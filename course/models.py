from django.db import models
from account.models import User
from account.models import colleges
# Create your models here.


weeks = [
    (1, '星期一'),
    (2, '星期二'),
    (3, '星期三'),
    (4, '星期四'),
    (5, '星期五'),
]

times = [
    (1, '08:00-09:50'),
    (2, '09:10-12:00'),
    (3, '13:30-15:10'),
    (4, '15:20-17:00'),
    (5, '19:00-21:00'),
]

classrooms = [
    (1, 'A101'),
    (2, 'A102'),
    (3, 'A103'),
    (4, 'A104'),
    (5, 'A105'),
    (6, 'A106'),
    (7, 'A201'),
    (8, 'A202'),
    (9, 'A203'),
    (10, 'A204'),
    (11, 'A205'),
    (12, 'A206'),
    (13, 'A301'),
    (14, 'A302'),
    (15, 'A303'),
    (16, 'A304'),
    (17, 'A305'),
    (18, 'A306'),
    (19, 'A306'),
    (20, 'A401'),
    (21, 'A402'),
    (22, 'A403'),
    (23, 'A501'),
    (24, 'A502'),
    (25, 'A503'),
    (26, 'A504'),
    (27, 'A505'),
    (28, 'A506'),
    (29, 'A507'),
    (30, 'A508'),
    (31, 'B101'),
    (32, 'B102'),
    (33, 'B103'),
    (34, 'B104'),
    (35, 'B105'),
    (36, 'B106'),
    (37, 'B201'),
    (38, 'B202'),
    (39, 'B203'),
    (40, 'B204'),
    (41, 'B205'),
    (42, 'B206'),
    (43, 'B301'),
    (44, 'B302'),
    (45, 'B303'),
    (46, 'B304'),
    (47, 'B305'),
    (48, 'B306'),
    (49, 'B306'),
    (50, 'B401'),
    (51, 'B402'),
    (52, 'B403'),
    (53, 'B501'),
    (54, 'B502'),
    (55, 'B503'),
    (56, 'B504'),

]


class Course(models.Model):
    course_no = models.CharField(max_length=10, db_index=True, unique=True)
    course_name = models.CharField(max_length=32, db_index=True)
    # 小数，最大为5
    course_credit = models.DecimalField(max_digits=2, decimal_places=1)
    course_ctime = models.DateTimeField(auto_now_add=True)
    course_desc = models.CharField(max_length=140, default='暂无', null=True)
    course_college = models.IntegerField(choices=colleges, default=1, verbose_name="开课学院")
    # 0=已发布 1=已被申请待审批 2=审批同意 3=审批拒绝 4=教师上线课程 5=课程关闭
    course_status = models.IntegerField(default=0)
    course_online = models.BooleanField(default=False)
    course_online_time = models.DateTimeField(null=True)
    course_starter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='pub_courses',
                                       blank=True)
    course_approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approve_courses',
                                        blank=True)
    # teacher add
    course_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apply_courses', null=True,
                                       blank=True)
    course_applied_time = models.DateTimeField(null=True)
    course_week = models.IntegerField(choices=weeks, default=1)
    course_time = models.IntegerField(choices=times, default=1)
    course_classroom = models.IntegerField(choices=classrooms, default=1)
    course_total_people = models.IntegerField(null=True)
    course_type = models.IntegerField(choices=[(1, '专业课'), (2, '公选课')], default=1)
    # 课程关闭时间, 默认是审批 上线后 3天后 自动关闭选课并下线
    course_close_time = models.DateTimeField(null=True, blank=True)
    course_choosed_student = models.IntegerField(default=0)

    class Meta:
        unique_together = ('course_teacher', 'course_week', 'course_time')


# 学生选课表
class StudentCourse(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    ctime = models.DateField(auto_now_add=True)
    is_choosed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'course')
