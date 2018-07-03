# Generated by Django 2.0.7 on 2018-07-03 09:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='place',
            field=models.IntegerField(
                choices=[(1, '助教'), (2, '讲师'), (3, '高级讲师'), (4, '副教授'), (5, '教授'), (6, '高级教授'), (7, '特聘教授'),
                         (8, '客座教授')], null=True),
        ),
    ]
