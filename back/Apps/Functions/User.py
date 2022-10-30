'''
Author: LetMeFly
Date: 2022-10-28 18:04:15
LastEditors: LetMeFly
LastEditTime: 2022-10-30 18:28:53
'''
from django.http import JsonResponse
from Apps import models
from Apps.Functions import Mail
import datetime
import random
import re


def baseInfo(request):
    warrant1024 = request.POST.get("warrant1024", "")
    if not warrant1024:
        return JsonResponse({"login": False})
    result = models.Cookie.objects.filter(warrant1024=warrant1024)
    if not len(result):
        return JsonResponse({"login": False})
    username = result.first().username
    result = models.User.objects.filter(username=username)
    lastGot = result.first().lastGot
    return JsonResponse({
        "username": username,
        "cardNotShare": str(lastGot) if lastGot else ""
    })



def cards(request):
    # "TEST"
    # return JsonResponse({
    #     "shared": [123, 542],
    #     "got": [120, 521],
    #     "error": [542],
    # })
    shared = []
    error = []
    got = []
    warrant1024 = request.GET.get("warrant1024", "")
    if not warrant1024:
        return JsonResponse({
            "shared": shared,
            "got": got,
            "error": error
        })
    result = models.Cookie.objects.filter(warrant1024=warrant1024)
    if not len(result):
        return JsonResponse({
            "shared": shared,
            "got": got,
            "error": error
        })
    username = result.first().username
    result = models.Cards.objects.filter(shareBy=username)
    for thisCard in result:
        shared.append(thisCard.cardID)
        if thisCard.get1 == 2 or thisCard.get2 == 2 or thisCard.get3 == 2:
            error.append(thisCard.cardID)
    result = models.Got.objects.filter(gotBy=username)
    for thisCard in result:
        got.append(thisCard.gotCardID)
    return JsonResponse({
        "shared": shared,
        "got": got,
        "error": error
    })


def login(request):  # 不考虑已登录状态下的再登录
    data = request.POST
    username = data.get("username", "")
    password = data.get("password", "")
    if (not username) or (not password):
        return JsonResponse({
            "warrant1024": "",
            "message": "There isn't a username or password in the request"
        })
    result = models.User.objects.filter(username=username)
    if not result:
        return JsonResponse({
            "warrant1024": "",
            "message": "No such user"
        })
    if result.first().password != password:
        return JsonResponse({
            "warrant1024": "",
            "message": "Username or password wrong"
        })
    warrant1024 = "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(20))
    models.Cookie.objects.create(warrant1024=warrant1024, username=username)
    return JsonResponse({
        "warrant1024": warrant1024
    })


def logout(request):  # 未考虑是否已经登录
    if request.method == "POST":
        warrant1024 = request.POST.get("warrant1024", "")
        if warrant1024:
            models.Cookie.objects.filter(warrant1024=warrant1024).delete()
        return JsonResponse({
            "response": "ok"
        })


def register(request):
    def ifAviliableUsername(username) -> bool:
        """
        只判断是否合法的名字，并判断是否已经存在
        """
        if len(username) < 1 or len(username) > 10:
            return False
        if '\'' in username or '"' in username:
            return False
        if len(models.User.objects.filter(username=username)):
            return False
        return True
    
    def ifAviliablePassword(password) -> bool:
        """
        只判断是否合法的密码
        """
        if len(password) > 20 or len(password) < 1:
            return False
        for c in password:
            if ord('a') <= ord(c) <= ord('z') or ord('A') <= ord(c) <= ord('Z') or ord('0') <= ord(c) <= ord('9'):
                pass
            else:
                return False
        return True
    
    def ifAviliableEmail(email) -> bool:
        """
        只判断是否合法的邮箱，并判断是否已经存在
        """
        if re.match("^\w{1,}(\.\w+)*@[A-z0-9]+(\.[A-z]{2,5}){1,2}$", email):
            if len(models.User.objects.filter(email=email)):
                return False
            return True
        return False
    
    def ifAviliableVericodeAndDelete(email, vericode):
        """
        判断是否是合法验证码，(正确、5min内)
        """
        result = models.Email.objects.filter(email=email)
        if len(result) == 0:
            return False
        if vericode != result.first().code:
            return False
        timeDelta = datetime.datetime.now() - result.first().lastSentTime
        timeDiff = timeDelta.seconds + timeDelta.days * 24 * 3600
        if timeDiff > 60 * 5:  # 5分钟
            return False
        result.delete()
        return True
    
    data = request.POST
    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")
    code = data.get("code", "")
    if (not username) or (not ifAviliableUsername(username=username)):
        return JsonResponse({
            "warrant1024": "",
            "message": "Username unavailable"
        })
    if (not email) or (not ifAviliableEmail(email=email)):
        return JsonResponse({
            "warrant1024": "",
            "message": "Email unavailable"
        })
    if (not password) or (not ifAviliablePassword(password=password)):
        return JsonResponse({
            "warrant1024": "",
            "message": "Password unavailable"
        })
    if (not code) or (not ifAviliableVericodeAndDelete(email=email, vericode=code)):
        return JsonResponse({
            "warrant1024": "",
            "message": "Verification Code unavailable"
        })
    models.User.objects.create(username=username, password=password, email=email)
    warrant1024 = "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for i in range(20))
    models.Cookie.objects.create(warrant1024=warrant1024, username=username)
    return JsonResponse({
        "warrant1024": warrant1024
    })


def register_sendCode(request):
    email = request.POST.get("email", "")
    if (not email) or (not re.match("^\w{1,}(\.\w+)*@[A-z0-9]+(\.[A-z]{2,5}){1,2}$", email)):
        return JsonResponse({
            "response": "",
            "message": "Email unavailable"
        })
    resultDB = models.Email.objects.filter(email=email)
    if len(resultDB):  # 表中已有此邮件对应的记录
        lastSentTime = resultDB.first().lastSentTime
        """ datetime.timedelta: 秒、天 """
        timeDelta = datetime.datetime.now() - lastSentTime
        timeDiff = timeDelta.seconds + timeDelta.days * 24 * 3600
        if timeDiff < 60 * 5:  # 5分钟
            return JsonResponse({
                "response": "",
                "message": "Request too fast"
            })
    code = "".join(str(random.randint(0, 9)) for i in range(6))
    resultEmail = Mail.sendEmail(toWho=email, title="Share1024 验证码", text="亲爱的用户，您正在注册“Share1024”，您的验证码为：" + code + "，5min内有效，打死也不要告诉他人哦")
    if resultEmail:
        if len(resultDB):
            resultDB.update(code=code, lastSentTime=datetime.datetime.now())
        else:
            models.Email.objects.create(email=email, code=code)
        return JsonResponse({
            "response": "ok"
        })
    else:
        return JsonResponse({
            "response": "",
            "message": "Email send failed"
        })

