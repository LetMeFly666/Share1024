'''
Author: LetMeFly
Date: 2022-10-28 11:46:50
LastEditors: LetMeFly
LastEditTime: 2022-11-05 09:11:24
'''
from django.db import models

# Create your models here.


class Email(models.Model):
    email = models.EmailField(verbose_name="邮箱", max_length=50, unique=True)
    lastSentTime = models.DateTimeField(verbose_name="最后一次发送时间", auto_now_add=True)
    code = models.CharField(verbose_name="验证码", max_length=8)

class User(models.Model):
    username = models.CharField(verbose_name="力扣id", max_length=30, unique=True)
    password = models.CharField(verbose_name="密码", max_length=20)
    email = models.EmailField(verbose_name="邮箱", max_length=50, unique=True)
    shareNum = models.IntegerField(verbose_name="一共分享了多少卡牌", default=0)
    cannotUseTimes = models.IntegerField(verbose_name="被反馈链接不能使用的次数", default=0)
    lastGot = models.IntegerField(verbose_name="上次领取的卡牌ID", default=0)  # 若已分享回来，则此值为0

class Cards(models.Model):
    cardID = models.AutoField(verbose_name="卡牌ID", primary_key=True)
    shareBy = models.CharField(verbose_name="被谁分享", max_length=30)  # Link to username
    cardIs = models.CharField(verbose_name="卡牌是什么", max_length=4)
    get1 = models.IntegerField(verbose_name="第一次领取", default=0)  #   | 0：待领取
    get2 = models.IntegerField(verbose_name="第二次领取", default=0)  # --| 1：已领取
    get3 = models.IntegerField(verbose_name="第三次领取", default=0)  #   | 2：被报无效
    gotTimes = models.IntegerField(verbose_name="被领取了几次", default=0)
    leetcodeURL = models.CharField(verbose_name="卡牌分享链接", max_length=100)

class Got(models.Model):
    gotCardID = models.IntegerField(verbose_name="被领取卡牌ID")
    gotBy = models.CharField(verbose_name="被谁领取", max_length=30)  # Link to username
    shareCardID = models.IntegerField(verbose_name="传递的卡牌ID", default=0)
    state = models.IntegerField(verbose_name="状态", default=0)  # 0：已领取  1：已分享  2：报无效
    th = models.IntegerField(verbose_name="此卡的第几次被领取")

class Cookie(models.Model):
    warrant1024 = models.CharField(verbose_name="warrant", max_length=20)
    username = models.CharField(verbose_name="被谁领取", max_length=30)  # Link to username
