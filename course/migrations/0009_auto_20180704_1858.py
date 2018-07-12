# Generated by Django 2.0.7 on 2018-07-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20180704_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_classroom',
            field=models.IntegerField(choices=[(1, 'A101'), (2, 'A102'), (3, 'A103'), (4, 'A104'), (5, 'A105'), (6, 'A106'), (7, 'A201'), (8, 'A202'), (9, 'A203'), (10, 'A204'), (11, 'A205'), (12, 'A206'), (13, 'A301'), (14, 'A302'), (15, 'A303'), (16, 'A304'), (17, 'A305'), (18, 'A306'), (19, 'A306'), (20, 'A401'), (21, 'A402'), (22, 'A403'), (23, 'A501'), (24, 'A502'), (25, 'A503'), (26, 'A504'), (27, 'A505'), (28, 'A506'), (29, 'A507'), (30, 'A508'), (31, 'B101'), (32, 'B102'), (33, 'B103'), (34, 'B104'), (35, 'B105'), (36, 'B106'), (37, 'B201'), (38, 'B202'), (39, 'B203'), (40, 'B204'), (41, 'B205'), (42, 'B206'), (43, 'B301'), (44, 'B302'), (45, 'B303'), (46, 'B304'), (47, 'B305'), (48, 'B306'), (49, 'B306'), (50, 'B401'), (51, 'B402'), (52, 'B403'), (53, 'B501'), (54, 'B502'), (55, 'B503'), (56, 'B504')], default=1),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_time',
            field=models.IntegerField(choices=[(1, '08:00-09:50'), (2, '09:10-12:00'), (3, '13:30-15:10'), (4, '15:20-17:00'), (5, '19:00-21:00')], default=1),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_total_people',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_type',
            field=models.IntegerField(choices=[(1, '专业课'), (2, '公选课')], default=1),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_week',
            field=models.IntegerField(choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五')], default=1),
        ),
    ]
