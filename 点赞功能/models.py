from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class 点赞总数类(models.Model):
	内容类型方法 = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	对象id方法 = models.PositiveIntegerField()
	内容对象方法 = GenericForeignKey('内容类型方法', '对象id方法')

	点赞数量方法 = models.IntegerField(default=0)

class 谁点赞类(models.Model):
	内容类型方法 = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	对象id方法 = models.PositiveIntegerField()
	内容对象方法 = GenericForeignKey('内容类型方法', '对象id方法')

	谁点赞方法 = models.ForeignKey(User,on_delete=models.CASCADE)
	点赞时间方法 = models.DateTimeField(auto_now_add=1)