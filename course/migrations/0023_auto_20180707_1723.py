# Generated by Django 2.0.7 on 2018-07-07 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0022_auto_20180707_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_total_people',
            field=models.IntegerField(default=0),
        ),
    ]
