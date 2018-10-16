from django.contrib import admin
from .models import 点赞总数类,谁点赞类

@admin.register(点赞总数类)
class 点赞总数类(admin.ModelAdmin):
    list_display = ('内容对象方法','点赞数量方法',)

@admin.register(谁点赞类)
class 点赞总数类(admin.ModelAdmin):
    list_display = ('内容对象方法','谁点赞方法',)