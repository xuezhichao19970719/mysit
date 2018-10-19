"""个人网站项目 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor',include('ckeditor_uploader.urls')),
    path('',views.首页函数,name='首页'),
    path('博客/',include('博客应用.urls')),
    path('评论/',include('评论功能.urls')),
    path('点赞/',include('点赞功能.urls')),
    path('登陆框登录/',views.登陆框登录函数,name='登陆框登录'),
    path('注册/',views.注册函数,name='注册'),
    path('退出登录/',views.退出登录函数,name='退出登录'),
    path('个人信息/',views.个人信息函数,name='个人信息'),
    path('修改密码/',views.修改密码函数,name='修改密码'),
    path('忘记密码/',views.忘记密码函数,name='忘记密码'),
    path('发送邮件/',views.发送邮件函数,name='发送邮件'),
    path('简历/',views.简历函数,name='简历'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)