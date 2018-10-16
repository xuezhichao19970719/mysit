import datetime,random,string,time,threading
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from 阅读统计.models import 计数类,计数信息类
from 博客应用.models import 博客类
from .models import 简介类
from .forms import 登录表单类,注册表单类,修改信息表单类,修改密码表单类,忘记密码表单类

def 本周阅读数量函数(内容类型方法):
	现在时间 = timezone.now().date()
	七日日期列表 = []
	七日阅读量列表 = []
	for i in range (7,0,-1):
		时间 = 现在时间 - datetime.timedelta(days=i)
		同一日阅读数量 = 计数信息类.objects.filter(内容类型方法=内容类型方法,日期信息方法=时间).aggregate(同一日阅读数量=Sum('阅读计数方法'))['同一日阅读数量']
		七日日期列表.append(时间.strftime("%m/%d"))
		七日阅读量列表.append(同一日阅读数量 or 0)
	return 七日阅读量列表,七日日期列表

def 昨日热点函数(内容类型方法):
	昨日日期 = timezone.now().date() - datetime.timedelta(days=1)
	昨日阅读数量排序 = 计数信息类.objects.filter(内容类型方法=内容类型方法,日期信息方法=昨日日期).order_by('-阅读计数方法')
	return 昨日阅读数量排序[:5]

def 一周热点函数(内容类型方法):
	现在时间 = timezone.now().date()
	七日前时间 = 现在时间 - datetime.timedelta(days=7)
	七日阅读数量排序 = 计数信息类.objects.filter(内容类型方法=内容类型方法,日期信息方法__gte=七日前时间).values('内容类型方法','对象id方法').annotate(一周阅读数量=Sum('阅读计数方法')).order_by('-一周阅读数量')
	一周热点博客字典 = {}
	for i in 七日阅读数量排序[:5]:
		博客 = get_object_or_404(博客类,pk=i['对象id方法'])
		一周热点博客字典.setdefault(博客,i['一周阅读数量'])
	return 一周热点博客字典

def 首页函数(request):
	内容类型 = ContentType.objects.get_for_model(博客类)
	七日博客阅读量列表,七日日期列表 = 本周阅读数量函数(内容类型)

	#获取 一周热点函数 缓存数据
	一周热点博客字典 = cache.get('一周热点博客')
	if not 一周热点博客字典:
		一周热点博客字典 =  一周热点函数(内容类型)
		cache.set('一周热点博客字典',一周热点博客字典,3600)

	昨日热点博客 = 昨日热点函数(内容类型)
	总阅读数量排序 = 计数类.objects.all().order_by('-阅读计数方法')[:5]
	return render(request,'首页.html',{'七日博客阅读量列表':七日博客阅读量列表,'七日日期列表':七日日期列表,'昨日热点博客':昨日热点博客,'一周热点博客字典':一周热点博客字典,'总阅读数量排序':总阅读数量排序})

def 退出登录函数(request):
	logout(request)
	return redirect(request.GET.get('from',reverse('首页')))

def 个人信息函数(request):
	if request.method == 'POST':
		修改信息表单 = 修改信息表单类(request.POST,request=request)
		if 修改信息表单.is_valid():
			新的昵称 = 修改信息表单.cleaned_data['新的昵称']
			新的邮箱 = 修改信息表单.cleaned_data['新的邮箱']
			用户 = request.user
			用户.email = 新的邮箱
			用户.save()
			简介 = 简介类.objects.get_or_create(user=用户)[0]
			简介.昵称方法 = 新的昵称
			简介.save()
			del request.session['邮箱验证码']
			return redirect(request.GET.get('from',reverse('首页')))
		else:
			return render(request,'个人信息页面.html',{'修改信息表单':修改信息表单})
	else: 
		简介 = 简介类.objects.filter(user=request.user)
		if 简介:
			原有昵称 = 简介[0].昵称方法
		else:
			原有昵称 = ''
		原有邮箱 = request.user.email
		修改信息表单 = 修改信息表单类(initial={'新的昵称': 原有昵称,'新的邮箱':原有邮箱})
		return render(request,'个人信息页面.html',{'修改信息表单':修改信息表单})

def 登陆框登录函数(request):
	登录表单 = 登录表单类(request.POST)
	if 登录表单.is_valid():
		用户 = 登录表单.cleaned_data['用户']
		login(request, 用户)
		return JsonResponse({'状态':'成功'})
	else:
		return JsonResponse({'状态':'错误'})

def 注册函数(request):
	if request.method == 'POST':
		注册表单 = 注册表单类(request.POST,request=request)
		if 注册表单.is_valid():
			注册用户名 = 注册表单.cleaned_data['注册用户名']
			邮箱 = 注册表单.cleaned_data['邮箱']
			注册密码 = 注册表单.cleaned_data['注册密码']
			用户 = User()
			用户.username = 注册用户名
			用户.email = 邮箱
			用户.set_password(注册密码)
			用户.save()
			login(request, 用户)
			del request.session['邮箱验证码']
			return redirect(reverse('个人信息'))
	else:
		注册表单 = 注册表单类()

	return render(request,'注册页面.html',{'注册表单':注册表单})

def 发送邮件函数(request):
	邮箱 = request.GET.get('邮箱','')
	data = {}
	if 邮箱 != '':
		#生成验证码
		邮箱验证码 = ''.join(random.sample(string.ascii_letters + string.digits,4))		
		now = int(time.time())
		发送时间 = request.session.get('发送时间',0)
		if now - 发送时间 < 30:
			data['状态'] = '错误'
		#发送邮件
		else:
			request.session['邮箱验证码'] = 邮箱验证码
			request.session['发送时间'] = 发送时间
			t = threading.Thread(target=send_mail, args=('邮箱验证','验证码： %s' % 邮箱验证码,'767366925@qq.com',[邮箱]),kwargs={'fail_silently':False,})
			t.start()
		data['状态'] = '成功'
	else:
		data['状态'] = '错误'
	return JsonResponse(data)

def 修改密码函数(request):
	if request.method == 'POST':
		修改密码表单 = 修改密码表单类(request.POST,request=request)
		if 修改密码表单.is_valid():
			新的密码 = 修改密码表单.cleaned_data['新的密码']
			用户 = request.user
			用户.set_password(新的密码)
			用户.save()
			logout(request)
			return redirect(reverse('首页'))
	else: 
		修改密码表单 = 修改密码表单类()

	return render(request,'修改密码页面.html',{'修改密码表单':修改密码表单})

def 忘记密码函数(request):
	if request.method == 'POST':
		忘记密码表单 = 忘记密码表单类(request.POST,request=request)
		if 忘记密码表单.is_valid():
			新的密码 = 忘记密码表单.cleaned_data['新的密码']
			邮箱 = 忘记密码表单.cleaned_data['邮箱']
			用户 = User.objects.get(email=邮箱)
			用户.set_password(新的密码)
			用户.save()
			del request.session['邮箱验证码']
			return redirect(reverse('首页'))
	else: 
		忘记密码表单 = 忘记密码表单类()

	return render(request,'忘记密码页面.html',{'忘记密码表单':忘记密码表单})