from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from 阅读统计.models import 计数类,计数信息类
from 评论功能.models import 评论类
from 点赞功能.models import 点赞总数类

class 博客类型类(models.Model):
    类型名称方法 = models.CharField(max_length=15)

    def __str__(self):
        return self.类型名称方法


class 博客类(models.Model):
    标题方法 = models.CharField(max_length=50)
    类型方法 = models.ForeignKey(博客类型类,on_delete=models.CASCADE)
    内容方法 = RichTextUploadingField()
    作者方法 = models.ForeignKey(User,on_delete=models.CASCADE)
    创建时间方法 = models.DateTimeField(auto_now_add=1)
    修改时间方法 = models.DateTimeField(auto_now=1)

    class Meta:
        ordering = ['-创建时间方法']

    def 阅读计数方法(self):
        阅读计数 = 计数类.objects.get_or_create(内容类型方法=ContentType.objects.get_for_model(self), 对象id方法=self.pk)[0]
        return 阅读计数.阅读计数方法

    def 评论计数方法(self):
        该博客下评论列表 = 评论类.objects.filter(内容类型方法=ContentType.objects.get_for_model(self),对象id方法=self.pk,回复哪条评论或回复方法=None)
        return 该博客下评论列表.count()

    def 被点赞数方法(self):
        被点赞数 = 点赞总数类.objects.get_or_create(内容类型方法=ContentType.objects.get_for_model(self), 对象id方法=self.pk)[0]
        return 被点赞数.点赞数量方法
    
    def __str__(self):
        return '博客标题：%s' % self.标题方法