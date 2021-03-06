# Generated by Django 2.0.7 on 2018-07-04 06:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import extra_app.DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='wathcer',
        ),
        migrations.AddField(
            model_name='news',
            name='watcher',
            field=models.IntegerField(choices=[(1, '所有人'), (2, '仅老师'), (3, '仅学生')], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=extra_app.DjangoUeditor.models.UEditorField(max_length=6000, verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_by',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]
