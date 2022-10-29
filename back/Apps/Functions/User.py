'''
Author: LetMeFly
Date: 2022-10-28 18:04:15
LastEditors: LetMeFly
LastEditTime: 2022-10-29 13:59:49
'''
from django.http import JsonResponse
from django.shortcuts import redirect
from Apps import models
from Apps.Functions import Mail
import datetime
import random
import re


def baseInfo(request):
    username = request.session.get("username", "")
    if not username:
        return JsonResponse({"login": False})
    result = models.User.objects.filter(username=username)
    lastGot = result.first().lastGot
    return JsonResponse({
        "username": username,
        "cardNotShare": str(lastGot) if lastGot else ""
    })



def cards(request):
    username = request.session.get("username", "")
    if not username:
        return redirect("/login.html")
    result = models.Cards.objects.filter(username=username)
    shared = []
    error = []
    for thisCard in result:
        shared.append(thisCard.cardID)
        if thisCard.get1 == 2 or thisCard.get2 == 2 or thisCard.get3 == 2:
            error.append(thisCard.cardID)
    result = models.Got.objects.filter(gotBy=username)
    got = []
    for thisCard in result:
        got.append(thisCard.cardID)
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
            "response": "fail",
            "message": "There isn't a username or password in the request"
        })
    result = models.User.objects.filter(username)
    if not result:
        return JsonResponse({
            "response": "fail",
            "message": "No such user"
        })
    if result.first().password != password:
        return JsonResponse({
            "response": "fail",
            "message": "Username or password wrong"
        })
    request.session["username"] = username
    return JsonResponse({
        "response": "ok"
    })


def logout(request):
    if request.method == "POST":
        request.session.clear()
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
            "response": "fail",
            "message": "Username unavailable"
        })
    if (not email) or (not ifAviliableEmail(email=email)):
        return JsonResponse({
            "response": "fail",
            "message": "Email unavailable"
        })
    if (not password) or (not ifAviliablePassword(password=password)):
        return JsonResponse({
            "response": "fail",
            "message": "Password unavailable"
        })
    if (not code) or (not ifAviliableVericodeAndDelete(email=email, vericode=code)):
        return JsonResponse({
            "response": "fail",
            "message": "Verification Code unavailable"
        })
    models.User.objects.create(username=username, password=password, email=email)
    request.session["username"] = username
    return JsonResponse({
        "response": "ok"
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

