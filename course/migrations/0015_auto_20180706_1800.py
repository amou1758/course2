# Generated by Django 2.0.7 on 2018-07-06 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_auto_20180706_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentcourse',
            name='score',
            field=models.IntegerField(null=True),
        ),
    ]
