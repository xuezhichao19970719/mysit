from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class 登录表单类(forms.Form):
	用户名或邮箱 = forms.CharField(label='用户名或邮箱',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名或邮箱'}))
	密码 = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))

	def clean(self):
		用户名或邮箱 = self.cleaned_data['用户名或邮箱']
		密码 = self.cleaned_data['密码']
		用户 = authenticate(username=用户名或邮箱, password=密码)
		if 用户:
			self.cleaned_data['用户'] = 用户
		elif User.objects.filter(email=用户名或邮箱).exists():
			用户名 = User.objects.get(email=用户名或邮箱).username
			用户 = authenticate(username=用户名, password=密码)
			if 用户:
				self.cleaned_data['用户'] = 用户
			else:
				raise forms.ValidationError('用户名或密码错误')
		else:
			raise forms.ValidationError('用户名或密码错误')
		return self.cleaned_data

class 注册表单类(forms.Form):
	注册用户名 = forms.CharField(label='用户名',max_length=15,min_length=3,widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "请输入用户名"}))
	邮箱 = forms.EmailField(required=False,label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control', "placeholder": "请输入邮箱"}))
	注册密码	 = forms.CharField(label='密码',max_length=15,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control', "placeholder": "请输入密码"}))
	重复密码 = forms.CharField(label='在输入一次密码',max_length=15,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control', "placeholder": "在输入一次密码"}))
	验证码 = forms.CharField(required=False,label='验证码',max_length=4,min_length=4,widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "请输入邮箱收到的验证码"}))

	def __init__(self,*args,**kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(注册表单类,self).__init__(*args,**kwargs)

	def clean_注册用户名(self):
		注册用户名 = self.cleaned_data['注册用户名']
		if User.objects.filter(username=注册用户名).exists():
			raise forms.ValidationError('用户名已存在')
		return 注册用户名

	def clean_邮箱(self):
		邮箱 = self.cleaned_data['邮箱']
		if User.objects.filter(email=邮箱).exists() and 邮箱:
			raise forms.ValidationError('邮箱已注册')
		return 邮箱

	def clean_重复密码(self):
		注册密码 = self.cleaned_data['注册密码']
		重复密码 = self.cleaned_data['重复密码']
		if 注册密码 != 重复密码:
			raise forms.ValidationError('两次输入密码不一致')
		return 注册密码

	def clean_验证码(self):
		邮箱 = self.data.get('邮箱','')
		验证码 = self.cleaned_data['验证码'].strip()
		if 验证码 =='' and 新的邮箱 != '':
			raise forms.ValidationError('验证码不能为空')
		if self.request.session.get('邮箱验证码','') != 验证码:
			raise forms.ValidationError('验证码错误')
		return 验证码

class 修改信息表单类(forms.Form):
	新的昵称 = forms.CharField(label='昵称',max_length=10,min_length=3,widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "请输入新昵称"}))
	新的邮箱 = forms.EmailField(required=False,label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control', "placeholder": "请输入新邮箱"}))
	验证码 = forms.CharField(required=False,label='验证码',max_length=4,min_length=4,widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "请输入邮箱收到的验证码"}))

	def __init__(self,*args,**kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(修改信息表单类,self).__init__(*args,**kwargs)

	def clean_新的昵称(self):
		新的昵称 = self.cleaned_data['新的昵称'].strip()
		if 新的昵称 == '':
			raise forms.ValidationError('新的昵称不能为空')
		return 新的昵称

	def clean_新的邮箱(self):
		新的邮箱 = self.cleaned_data['新的邮箱']
		if 新的邮箱 == '':
			return 新的邮箱
		if 新的邮箱 == self.request.user.email:
			return 新的邮箱
		if User.objects.filter(email=新的邮箱):
			raise forms.ValidationError('邮箱已注册')
		return 新的邮箱

	def clean_验证码(self):
		新的邮箱 = self.data.get('新的邮箱','')
		验证码 = self.cleaned_data['验证码'].strip()
		if 验证码 =='' and 新的邮箱 != '' and 新的邮箱 != self.request.user.email:
			raise forms.ValidationError('验证码不能为空')
		if self.request.session.get('邮箱验证码','') != 验证码 and 新的邮箱 != self.request.user.email:
			raise forms.ValidationError('验证码错误')
		return 验证码

class 修改密码表单类(forms.Form):
	旧的密码 = forms.CharField(label='旧的密码',max_length=15,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control', "placeholder": "请输入旧的密码"}))
	新的密码 = forms.CharField(label='新的密码',max_length=15,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control', "placeholder": "请输入新的密码"}))
	重复新的密码 = forms.CharField(label='重复新的密码',max_length=15,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control', "placeholder": "请重复输入新的密码"}))

	def __init__(self,*args,**kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(修改密码表单类,self).__init__(*args,**kwargs)

	def clean(self):
		#验证新的密码是否一致
		新的密码 = self.cleaned_data.get('新的密码','')
		重复新的密码 = self.cleaned_data.get('重复新的密码','')

		if 新的密码 != 重复新的密码 or 新的密码 == '':
			raise forms.ValidationError('两次输入密码不一致')
		return self.cleaned_data

	def clean_旧的密码(self):
		旧的密码 = self.cleaned_data.get('旧的密码','')
		if not self.request.user.is_authenticated:
			raise forms.ValidationError('请登录后在操作')
		if not self.request.user.check_password(旧的密码):
			raise forms.ValidationError('旧的密码错误')
		return 旧的密码

class 忘记密码表单类(forms.Form):
	邮箱 = forms.EmailField(required=False,label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control', "placeholder": "请输入新邮箱"}))
	新的密码 = forms.CharField(label='新的密码',max_length=15,min_length=6,widget=forms.PasswordInput(attrs={'class':'form-control', "placeholder": "请输入新的密码"}))
	验证码 = forms.CharField(required=False,label='验证码',max_length=4,min_length=4,widget=forms.TextInput(attrs={'class':'form-control', "placeholder": "请输入邮箱收到的验证码"}))

	def __init__(self,*args,**kwargs):
		if 'request' in kwargs:
			self.request = kwargs.pop('request')
		super(忘记密码表单类,self).__init__(*args,**kwargs)

	def clean_邮箱(self):
		邮箱 = self.cleaned_data['邮箱']
		if not User.objects.filter(email=邮箱).exists():
			raise forms.ValidationError('邮箱不存在')
		return 邮箱

	def clean_新的密码(self):
		新的密码 = self.cleaned_data['新的密码']
		if 新的密码 == '':
			raise forms.ValidationError('请输入新的密码')
		return 新的密码

	def clean_验证码(self):
		验证码 = self.cleaned_data['验证码'].strip()
		if 验证码 =='':
			raise forms.ValidationError('验证码不能为空')
		if self.request.session.get('邮箱验证码','') != 验证码:
			raise forms.ValidationError('验证码错误')
		return 验证码