from django.contrib import admin
from .models import 计数类,计数信息类

@admin.register(计数类)
class 计数类(admin.ModelAdmin):
	 list_display = ('阅读计数方法','内容对象方法')

@admin.register(计数信息类)
class 计数信息类(admin.ModelAdmin):
	 list_display = ('日期信息方法','阅读计数方法','内容对象方法')