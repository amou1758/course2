# Generated by Django 2.0.7 on 2018-07-03 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180703_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.IntegerField(choices=[(1, '学生'), (2, '教师'), (3, '教务')], null=True),
        ),
    ]
