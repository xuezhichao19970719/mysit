from django.urls import path
from . import views

urlpatterns = [
	#http://127.0.0.1:8000/评论/提交评论/
    path('提交评论',views.提交评论函数,name='提交评论'),
	]