'''
Author: LetMeFly
Date: 2022-10-28 11:46:50
LastEditors: LetMeFly
LastEditTime: 2022-10-28 12:00:39
'''
from django.db import models

# Create your models here.


class Email(models.Model):
    email = models.EmailField(verbose_name="邮箱", max_length=50, unique=True)
    lastSentTime = models.DateTimeField(verbose_name="最后一次发送时间", auto_now_add=True)
    code = models.CharField(verbose_name="验证码", max_length=8)
