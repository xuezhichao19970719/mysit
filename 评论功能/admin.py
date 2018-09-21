from django.contrib import admin
from .models import 评论类

@admin.register(评论类)
class 评论类(admin.ModelAdmin):
    list_display = ('内容类型方法','对象id方法','内容对象方法','评论时间方法','评论人方法')