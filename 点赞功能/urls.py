from django.urls import path
from . import views

urlpatterns = [
	#http://127.0.0.1:8000/评论/提交评论/
    path('点赞与取消',views.点赞与取消函数,name='点赞与取消'),
	]