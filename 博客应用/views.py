from django.shortcuts import get_object_or_404,render
from django.core.paginator import Paginator
from django.db.models import Count,F
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import 博客类,博客类型类
from 阅读统计.models import 计数类,计数信息类
from 评论功能.models import 评论类
from 评论功能.forms import 评论表单类
from 个人网站项目.forms import 登录表单类

def 共同数据函数(request,所有相似博客):
    所有博客类型 = 博客类型类.objects.annotate(数量=Count('博客类'))
    所有博客日期 = 博客类.objects.dates('创建时间方法','month',order='DESC')
    博客日期与数量列表 = {}
    for 日期 in 所有博客日期:
        数量 = 博客类.objects.filter(创建时间方法__year=日期.year,创建时间方法__month=日期.month).count()
        博客日期与数量列表[日期] = 数量
    分页器 = Paginator(所有相似博客,7)
    页码 = request.GET.get('页码',1)
    对应博客页面 = 分页器.get_page(页码)
    博客列表 = 对应博客页面.object_list
    显示页码列表 = [x for x in range(对应博客页面.number-3,对应博客页面.number+4) if x in 分页器.page_range]
    return {'所有博客类型':所有博客类型,'博客日期与数量列表':博客日期与数量列表,'分页器':分页器,'对应博客页面':对应博客页面,'博客列表':博客列表,'显示页码列表':显示页码列表}

def 博客列表函数(request):
    所有相似博客 = 博客类.objects.all()
    返回字典 = 共同数据函数(request,所有相似博客)
    return render(request,'博客列表.html',返回字典)

def 博客类型函数(request,博客类型):
    所有相似博客 = 博客类.objects.filter(类型方法=博客类型)
    返回字典 = 共同数据函数(request,所有相似博客)
    返回字典['博客类型'] = get_object_or_404(博客类型类,pk=博客类型)
    return render(request,'相同类型博客列表.html',返回字典)

def 博客日期归档函数(request,年,月):
    所有相似博客 = 博客类.objects.filter(创建时间方法__year=年,创建时间方法__month=月)
    返回字典 = 共同数据函数(request,所有相似博客)
    返回字典['博客日期'] = '%s年%s月' % (年,月)
    return render(request,'博客日期归档.html',返回字典)

def 博客内容函数(request,博客ID):
    博客内容 = get_object_or_404(博客类,pk=博客ID)
    评论表单 = 评论表单类(initial={'内容类型':ContentType.objects.get_for_model(博客类),'对象id':博客ID,'回复哪条评论id':'0'})
    评论列表 = 评论类.objects.filter(内容类型方法=ContentType.objects.get_for_model(博客类),对象id方法=博客ID,回复哪条评论或回复方法=None).order_by('-评论时间方法')

    if not request.COOKIES.get('read_%s' % 博客ID):
        内容类型 = ContentType.objects.get_for_model(博客类)
        阅读计数 = 计数类.objects.get(内容类型方法=内容类型, 对象id方法=博客ID)
        阅读计数.阅读计数方法 = F('阅读计数方法') + 1
        阅读计数.save()

        当日阅读计数 = 计数信息类.objects.get_or_create(内容类型方法=内容类型,对象id方法=博客ID,日期信息方法=timezone.now())[0]
        当日阅读计数.阅读计数方法 = F('阅读计数方法') + 1
        当日阅读计数.save()

    上一篇博客 = 博客类.objects.filter(创建时间方法__gt=博客内容.创建时间方法).last
    下一篇博客 = 博客类.objects.filter(创建时间方法__lt=博客内容.创建时间方法).first
    响应 = render(request,'博客内容.html',{'博客内容':博客内容,'上一篇博客':上一篇博客,'下一篇博客':下一篇博客,'评论列表':评论列表,'评论表单':评论表单,})
    响应.set_cookie('read_%s' % 博客ID, 'true')
    return 响应