# Generated by Django 2.0.7 on 2018-07-12 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0027_auto_20180710_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourse',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
