# Generated by Django 2.0.7 on 2018-07-04 17:27

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0007_course_course_choosed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('course_teacher', 'course_week', 'course_time')},
        ),
    ]
