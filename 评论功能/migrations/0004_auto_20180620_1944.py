# Generated by Django 2.0.6 on 2018-06-20 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('评论功能', '0003_auto_20180618_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='评论类',
            name='回复哪个用户方法',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='回复哪个用户', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='评论类',
            name='回复哪条评论或回复方法',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='回复哪条评论或回复', to='评论功能.评论类'),
        ),
        migrations.AlterField(
            model_name='评论类',
            name='在哪条评论下回复方法',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='在哪条评论下回复', to='评论功能.评论类'),
        ),
    ]
