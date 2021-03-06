# Generated by Django 2.0.5 on 2018-06-04 13:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='计数信息类',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('日期信息方法', models.DateField(default=datetime.datetime(2018, 6, 4, 21, 25, 30, 251475))),
                ('阅读计数方法', models.IntegerField(default=0)),
                ('对象id方法', models.PositiveIntegerField()),
                ('内容类型方法', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='计数类',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('阅读计数方法', models.IntegerField(default=0)),
                ('对象id方法', models.PositiveIntegerField()),
                ('内容类型方法', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
