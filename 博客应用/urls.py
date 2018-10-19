from django.urls import path
from . import views

urlpatterns = [
	#http://127.0.0.1:8000/博客/
    path('',views.博客列表函数,name='博客链接列表'),
    #http://127.0.0.1:8000/博客/1
    path('<int:博客ID>',views.博客内容函数,name='博客内容'),
    #http://127.0.0.1:8000/博客/类型/1
    path('类型/<int:博客类型>',views.博客类型函数,name='博客类型'),
    #http://127.0.0.1:8000/博客/日期/1
    path('日期/<int:年>/<int:月>',views.博客日期归档函数,name='博客日期归档'),
	]