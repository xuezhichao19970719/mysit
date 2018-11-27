import datetime
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from 博客应用.models import 博客类,博客类型类
from 阅读统计.models import 计数信息类
from .views import 一周热点函数,昨日热点函数


class 热点博客测试(TestCase):
    @classmethod
    def setUpTestData(cls):
        print('setUpTestData:设置所有测试方法共用数据')

        内容类型 = ContentType.objects.get_for_model(博客类)
        测试用户1 = User.objects.create_user(username='测试用户1', password='123456')
        测试用户1.save()

        测试类型1 = 博客类型类.objects.create(类型名称方法='测试类型1')

        for 天数,阅读数 in zip(range(-10,4,3),range(5,0,-1)):
            创建时间方法 = timezone.now() + datetime.timedelta(days=天数)
            标题方法 = '标题：',天数
            内容方法 = '内容：',天数
            博客实例 = 博客类.objects.create(标题方法=标题方法,类型方法=测试类型1,内容方法=内容方法,作者方法=测试用户1,创建时间方法=创建时间方法)
            计数信息类.objects.create(内容类型方法=内容类型,对象id方法=博客实例.pk,阅读计数方法=阅读数,日期信息方法=创建时间方法)

    def test_创建博客数量(self):
        所有创建博客列表 = 博客类.objects.all()
        #print('所有创建的博客：',所有创建博客列表)
        创建博客数量 = len(所有创建博客列表)
        self.assertEqual(创建博客数量, 5)

    def test_一周热点函数(self):
        内容类型 = ContentType.objects.get_for_model(博客类)
        一周热点博客字典 = 一周热点函数(内容类型)
        print(一周热点博客字典)
        self.assertEqual(list(一周热点博客字典.values()),[4, 3, 2])
        print('一周前博客不在一周热点函数中，且排序正确')

    def test_昨日热点函数(self):
        内容类型 = ContentType.objects.get_for_model(博客类)
        昨日阅读数量排序 = 昨日热点函数(内容类型)
        self.assertEqual(len(昨日阅读数量排序),1) 
        self.assertEqual(昨日阅读数量排序[0],计数信息类.objects.get(pk=4)) 
        print('昨日没有博客阅读数')