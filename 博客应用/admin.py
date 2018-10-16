from django.contrib import admin
from .models import 博客类,博客类型类

@admin.register(博客类型类)
class 博客类型类(admin.ModelAdmin):
    list_display = ('id','类型名称方法',)

@admin.register(博客类)
class 博客类(admin.ModelAdmin):
    list_display = ('标题方法','类型方法','作者方法','创建时间方法','修改时间方法','阅读计数方法','被点赞数方法','id')