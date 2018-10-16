from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
from .models import 评论类
from .forms import 评论表单类

def 提交评论函数(request):
	用户 = request.user
	评论表单 = 评论表单类(request.POST)
	if 评论表单.is_valid() and 用户.is_authenticated:
		对象id = 评论表单.cleaned_data['对象id']
		内容类型 = 评论表单.cleaned_data['内容类型']
		评论内容 = 评论表单.cleaned_data['评论内容']
		评论 = 评论类()
		评论.评论人方法 = 用户
		评论.内容类型方法 = ContentType.objects.get(model=内容类型)
		评论.评论内容方法 = 评论内容
		评论.对象id方法 = 对象id
		回复哪条评论或回复 = 评论表单.cleaned_data['回复哪条评论或回复']
		if 回复哪条评论或回复:
			评论.在哪条评论下回复方法 = 回复哪条评论或回复 if 回复哪条评论或回复.在哪条评论下回复方法 is None else 回复哪条评论或回复.在哪条评论下回复方法
			评论.回复哪条评论或回复方法 = 回复哪条评论或回复
			评论.回复哪个用户方法 = 回复哪条评论或回复.评论人方法
			评论.save()
			return JsonResponse({
				'状态':'成功',
				'用户名':评论.评论人方法.昵称(),
				'评论时间':(评论.评论时间方法 + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
				'评论内容':评论.评论内容方法,
				'回复哪个用户':评论.回复哪个用户方法.昵称(),
				'pk':评论.在哪条评论下回复方法.pk
				})
		else:
			评论.save()
			return JsonResponse({
				'状态':'成功',
				'用户名':评论.评论人方法.昵称(),
				'评论时间':(评论.评论时间方法 + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
				'评论内容':评论.评论内容方法,
				'pk':评论.pk,
				})

	else:
		return JsonResponse({
			'状态':'错误',
			'错误信息':list(评论表单.errors.values())[0][0]
			})