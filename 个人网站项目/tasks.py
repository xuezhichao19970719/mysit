from celery.task import task
from django.core.mail import send_mail

@task(bind=True, max_retries=3, default_retry_delay=10)
def celery发送邮件(self,邮箱验证码,邮箱):
    try:
        send_mail('邮箱验证','验证码： %s' % 邮箱验证码,'767366925@qq.com',[邮箱],fail_silently=False)
    except Exception as e:
        #出错尝试重新执行1次
        raise self.retry(exc=e)