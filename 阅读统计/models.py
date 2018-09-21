from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from datetime import datetime

class 计数类(models.Model):
	阅读计数方法 = models.IntegerField(default=0)

	内容类型方法 = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	对象id方法 = models.PositiveIntegerField()
	内容对象方法 = GenericForeignKey('内容类型方法', '对象id方法')

	class Meta:
		ordering = ['id']

class 计数信息类(models.Model):
	日期信息方法 = models.DateField(default=timezone.now)
	阅读计数方法 = models.IntegerField(default=0)

	内容类型方法 = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	对象id方法 = models.PositiveIntegerField()
	内容对象方法 = GenericForeignKey('内容类型方法', '对象id方法')

	class Meta:
		ordering = ['-日期信息方法']