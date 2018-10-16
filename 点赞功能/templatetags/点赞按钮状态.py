from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import 点赞总数类,谁点赞类

register = template.Library()

@register.simple_tag(takes_context=True)
def 点赞按钮状态函数(context,obj):
	内容类型 = ContentType.objects.get_for_model(obj)
	if not context['user'].is_authenticated:
		return ''
	elif context['user'].is_authenticated and 谁点赞类.objects.filter(内容类型方法=内容类型,对象id方法=obj.pk,谁点赞方法=context['user']).exists():
		return 'active'
	else:
		return ''