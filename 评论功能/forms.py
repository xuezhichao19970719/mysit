from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import 评论类

class 评论表单类(forms.Form):
	内容类型 = forms.CharField(widget=forms.HiddenInput)
	对象id = forms.IntegerField(widget=forms.HiddenInput)
	评论内容 = forms.CharField(widget=CKEditorWidget(config_name='评论框'),error_messages={'required':'请评论后提交'})
	回复哪条评论或回复_id = forms.IntegerField(required=False,widget=forms.HiddenInput(attrs={'id':'回复哪条评论或回复_id','value':'0'}))

	def clean(self):
		内容类型 = self.cleaned_data['内容类型']
		对象id = self.cleaned_data['对象id']
		try:
			评论对象 = ContentType.objects.get(model=内容类型).model_class().objects.get(pk=对象id)
		except ObjectDoesNotExist:
			raise forms.ValidationError('评论对象不存在')
		return self.cleaned_data

	def clean_回复哪条评论或回复_id(self):
		回复哪条评论或回复_id = self.cleaned_data['回复哪条评论或回复_id']
		if 回复哪条评论或回复_id < 0:
			raise forms.ValidationError('回复出错')
		elif 回复哪条评论或回复_id == 0:
			self.cleaned_data['回复哪条评论或回复'] = None
		else:
			self.cleaned_data['回复哪条评论或回复'] = 评论类.objects.get(pk=回复哪条评论或回复_id)
		return self.cleaned_data