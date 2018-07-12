# Generated by Django 2.0.7 on 2018-07-04 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_course_college'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_college',
            field=models.IntegerField(choices=[(1, '新闻学院'), (2, '信息工程学院'), (3, '马克思研究学院'), (4, '医学院'), (5, '播音学院'), (6, '戏剧影视学院'), (7, '计算机学院'), (8, '外国语学院')], default=1, verbose_name='开课学院'),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_desc',
            field=models.CharField(default='暂无', max_length=140, null=True),
        ),
    ]
