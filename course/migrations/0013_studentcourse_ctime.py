# Generated by Django 2.0.7 on 2018-07-06 16:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_course_course_choosed'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcourse',
            name='ctime',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
