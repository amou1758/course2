# Generated by Django 2.0.7 on 2018-07-07 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0024_course_course_visable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='course_visable',
        ),
    ]
