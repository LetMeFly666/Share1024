'''
Author: LetMeFly
Date: 2022-10-27 10:55:40
LastEditors: LetMeFly
LastEditTime: 2022-10-31 13:52:35
'''
"""Let1024 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from Apps.Functions import Card
from Apps.Functions import User


def test(request):
    from Apps import models
    models.Cards.objects.create(shareBy="share", cardIs="card", leetcodeURL="ac.m")


urlpatterns = [
    # path('admin/', admin.site.urls),
    path("user/baseInfo/", User.baseInfo),
    path("user/cards/", User.cards),
    path("user/login/", User.login),
    path("user/logout/", User.logout),
    path("user/register/", User.register),
    path("user/register/sendCode/", User.register_sendCode),
    path("card/remain/all/", Card.remain_all),
    path("card/remain/typeAndID/", Card.remain_typeAndID),
    path("card/remain/oneType/", Card.remain_oneType),
    path("card/oneCard/", Card.oneCard),
    path("card/oneCard/getURL/", Card.oneCard_getURL),
    path("card/share/", Card.share),
    path("card/cannotUse/", Card.cannotUse),
    # path("test/", test),  # DEBUG
]
