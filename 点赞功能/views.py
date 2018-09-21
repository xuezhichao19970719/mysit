from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from .models import 点赞总数类,谁点赞类

def 点赞与取消函数(request):
	内容类型 = ContentType.objects.get(model=request.GET.get('内容类型'))
	对象id = int(request.GET.get('对象id'))
	点赞状态 = request.GET.get('点赞状态')
	谁点赞 = request.user
	if not 谁点赞.is_authenticated:
		return JsonResponse({
			'状态':'错误',
			'code':400,
			'错误信息':'请登录后点赞',
			})
	elif 点赞状态 == 'true':
		谁点赞,是否创建 = 谁点赞类.objects.get_or_create(内容类型方法=内容类型,对象id方法=对象id,谁点赞方法=谁点赞)
		if 是否创建:
			点赞总数 = 点赞总数类.objects.get_or_create(内容类型方法=内容类型,对象id方法=对象id)[0]
			点赞总数.点赞数量方法 += 1
			点赞总数.save()
			print(点赞总数.点赞数量方法)
			return JsonResponse({
				'状态':'成功',
				'点赞总数':点赞总数.点赞数量方法
				})
		else:
			#已点赞过
			return JsonResponse({
				'状态':'错误',
				'code':402,
				'错误信息':'你已经点赞过，无法继续点赞',
				})
	else:
		if 谁点赞类.objects.filter(内容类型方法=内容类型,对象id方法=对象id,谁点赞方法=谁点赞).exists():
			谁点赞类.objects.get(内容类型方法=内容类型,对象id方法=对象id,谁点赞方法=谁点赞).delete()
			点赞总数 = 点赞总数类.objects.get(内容类型方法=内容类型,对象id方法=对象id)
			点赞总数.点赞数量方法 -= 1
			点赞总数.save()
			print(点赞总数.点赞数量方法)
			return JsonResponse({
				'状态':'成功',
				'点赞总数':点赞总数.点赞数量方法
				})
		else:
			return JsonResponse({
				'状态':'错误',
				'code':402,
				'错误信息':'你没有点赞过，无法取消点赞',
				})