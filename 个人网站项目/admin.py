from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import 简介类

class 简介类Inline(admin.StackedInline):
    model = 简介类
    can_delete = False

class UserAdmin(BaseUserAdmin):
    inlines = (简介类Inline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(简介类)
class 简介类(admin.ModelAdmin):
    list_display = ('user','昵称方法')