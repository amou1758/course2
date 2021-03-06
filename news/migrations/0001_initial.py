# Generated by Django 2.0.7 on 2018-07-03 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('content', models.TextField(max_length=3000)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('mtime', models.DateTimeField(auto_now=True)),
                ('wathcer', models.CharField(choices=[('S', '学生'), ('T', '教师'), ('A', '所有人')], max_length=1)),
                ('created_by', models.ForeignKey(default='空缺', on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
                ('modify_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modify_news', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
