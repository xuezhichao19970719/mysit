from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from 点赞功能.models import 点赞总数类

class 评论类(models.Model):
	内容类型方法 = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	对象id方法 = models.PositiveIntegerField()
	内容对象方法 = GenericForeignKey('内容类型方法', '对象id方法')

	评论内容方法 = models.TextField()
	评论时间方法 = models.DateTimeField(auto_now_add=1)
	评论人方法 = models.ForeignKey(User,related_name='评论人',on_delete=models.CASCADE)
	在哪条评论下回复方法 = models.ForeignKey('self',related_name='在哪条评论下回复',null=True,blank=True,on_delete=models.CASCADE)
	回复哪条评论或回复方法 = models.ForeignKey('self',related_name='回复哪条评论或回复',null=True,blank=True,on_delete=models.CASCADE)
	回复哪个用户方法 = models.ForeignKey(User,related_name='回复哪个用户',null=True,blank=True,on_delete=models.CASCADE)

	def 被点赞数方法(self):
		被点赞数 = 点赞总数类.objects.get_or_create(内容类型方法=ContentType.objects.get_for_model(self), 对象id方法=self.pk)[0]
		return 被点赞数.点赞数量方法

	def __str__(self):
		return '回复对象：%s' % self.评论内容方法

	class Meta:
		ordering = ['评论时间方法']