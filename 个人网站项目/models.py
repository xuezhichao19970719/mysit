from django.db import models
from django.contrib.auth.models import User

class 简介类(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	昵称方法 = models.CharField(max_length=20, verbose_name='昵称')

	def __str__(self):
		return '用户 %s 的昵称 %s' %(self.user.username,self.昵称方法)

def 昵称函数(self):
	简介 = 简介类.objects.filter(user=self)
	if 简介:
		return 简介类.objects.filter(user=self)[0].昵称方法
	else:
		return self.username

User.昵称 = 昵称函数