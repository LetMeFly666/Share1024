'''
Author: LetMeFly
Date: 2022-10-28 18:04:22
LastEditors: LetMeFly
LastEditTime: 2022-10-30 19:11:40
'''
from django.http import JsonResponse
from django.shortcuts import redirect
from Apps import models


cardList = [
    "0", "1", "2", "3", "4", "5", "6", "007", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "955", "965", "996", "1024", "1075", "1037", "<<", ">>", "&", "|", "^", "+", "-", "*", "//", "%", "**"
]


def remain_all(request):
    result = models.Cards.objects.filter(gotTimes__lt=3)
    ans = {thisCard: 0 for thisCard in cardList}
    for thisCard in result:
        ans[thisCard.cardIs] += 1
    return JsonResponse(ans)


def remain_oneType(request):
    cardType = request.GET.get("cardType", "")
    if cardType not in cardList:
        return JsonResponse({
            "cards": []
        })
    result = models.Cards.objects.filter(cardIs=cardType).filter(gotTimes__lt=3)
    ans = []
    for thisCard in result:
        ans.append(thisCard.cardID)
    return JsonResponse({
        "cards": ans
    })


def oneCard(request):
    cardID = request.GET.get("cardID", "")
    if not cardID:
        return JsonResponse({
            "cardID": 0,
            "message": "Card doesn't exist"
        })
    result = models.Cards.objects.filter(cardID=cardID)
    if not len(result):
        return JsonResponse({
            "cardID": 0,
            "message": "Card doesn't exist"
        })
    return JsonResponse({
        "cardID": cardID,
        "cardType": result.first().cardIs,
        "shareBy": result.first().shareBy,
        "get1": result.first().get1,
        "get2": result.first().get2,
        "get3": result.first().get3,
        "gotTimes": result.first().gotTimes,
    })


def oneCard_getURL(request):
    warrant1024 = request.POST.get("warrant1024", "")
    if not warrant1024:
        return JsonResponse({
            "leetcodeURL": "",
            "message": "Please login first",
        })
    result = models.Cookie.objects.filter(warrant1024=warrant1024)
    if not len(result):
        return JsonResponse({
            "leetcodeURL": "",
            "message": "Please login first",
        })
    username = result.first().username
    user = models.User.objects.filter(username=username)
    if user.first().lastGot:
        return JsonResponse({
            "leetcodeURL": "",
            "message": "Please share back what you got",
            "shouldGo": "card1.html?cardID=" + str(user.first().lastGot)
        })
    cardID = request.POST.get("cardID", "")
    if not cardID:
        return JsonResponse({
            "leetcodeURL": "",
            "message": "Card doesn't exist"
        })
    card = models.Cards.objects.filter(cardID=cardID)
    if not len(card):
        return JsonResponse({
            "leetcodeURL": "",
            "message": "Card doesn't exist"
        })
    gotTimes = card.first().gotTimes
    if gotTimes > 2:
        return JsonResponse({
            "leetcodeURL": "",
            "message": "Too late, all cards were taken"
        })
    gotTimes += 1
    user.update(lastGot=cardID)
    if gotTimes == 1:
        card.update(gotTimes=gotTimes, get1=1)
    elif gotTimes == 2:
        card.update(gotTimes=gotTimes, get2=1)
    else:
        card.update(gotTimes=gotTimes, get3=1)
    # card.update({  # removed kwargs=
    #     "gotTimes": gotTimes,
    #     f"get{gotTimes}": 1
    # })
    models.Got.objects.create(gotCardID=cardID, gotBy=username, shareCardID=0, state=0, th=gotTimes)
    return JsonResponse({
        "leetcodeURL": card.first().leetcodeURL
    })



def share(request):
    username = request.session.get("username", "")
    if not username:
        return redirect("/login.html")
    user = models.User.objects.filter(username=username)
    lastGot = user.first().lastGot
    parentID = request.POST.get("parent", "")
    if lastGot and lastGot != parentID:
        return redirect("/card1.html?cardID=" + str(lastGot))
    leetcodeURL_original = request.POST.get("leetcodeURL", "")
    locFrom = leetcodeURL_original.find("https://leetcode.cn/2022-1024?id=")
    locID = locFrom + 33
    locUserSlugBegin = leetcodeURL_original.find("&userSlug=")
    locUserSlug = locUserSlugBegin + 10
    if locFrom == -1 or locUserSlugBegin == -1 or locID <= locUserSlugBegin or locUserSlug >= len(leetcodeURL_original) - 1:
        return JsonResponse({
            "newCardID": "",
            "message": "Not a right link"
        })
    cardID = leetcodeURL_original[locID : locUserSlugBegin]
    userSlug = ""
    for i in range(locUserSlug, len(leetcodeURL_original)):
        if ord('0') <= ord(i) <= ord('9') or ord('a') <= ord(i) <= ord('z') or ord('A') <= ord(i) <= ord('Z') or i == '-' or i == '_':
            userSlug += leetcodeURL_original[i]
        else:
            break
    if not cardID.isdecimal() or not userSlug:
        return JsonResponse({
            "newCardID": "",
            "message": "Not a right link"
        })
    leetcodeURL = f"https://leetcode.cn/2022-1024?id={cardID}&userSlug={userSlug}"
    cardType = request.POST.get("cardType", "")
    if cardType not in cardList:
        return JsonResponse({
            "newCardID": "",
            "message": "We don't have a cardType of this"
        })
    got = models.Got.objects.filter(gotCardID=parentID, gotBy=username)
    th = got.first().th
    user.update(lastGot=0, shareNum=user.first().shareNum + 1)
    newCard = models.Cards.objects.create(shareBy=username, cardIs=cardType, leetcodeURL=leetcodeURL)
    got.update(shareCardID=newCard.first().cardID)
    if th == 1:
        models.Cards.objects.filter(cardID=parentID).update(get1=1)
    elif th == 2:
        models.Cards.objects.filter(cardID=parentID).update(get2=1)
    else:
        models.Cards.objects.filter(cardID=parentID).update(get3=1)
    # models.Cards.objects.filter(cardID=parentID).update({  # removed kwargs=
    #     f"get{th}": 1
    # })
    return JsonResponse({
        "newCardID": newCard.first().cardID
    })
    

def cannotUse(request):
    warrant1024 = request.POST.get("warrant1024", "")
    if not warrant1024:
        return JsonResponse({
            "response": "",
            "message": "Please login first",
        })
    result = models.Cookie.objects.filter(warrant1024=warrant1024)
    if not len(result):
        return JsonResponse({
            "response": "",
            "message": "Please login first",
        })
    username = result.first().username
    user = models.User.objects.filter(username=username)
    lastGot = user.first().lastGot
    if not lastGot:
        return JsonResponse({
            "response": "",
            "message": "Sorry, you shouldn't report this card"
        })
    cardID = request.POST.get("cardID", "")
    print(lastGot, type(lastGot))
    print(cardID, type(cardID))
    if str(lastGot) != str(cardID):
        return JsonResponse({
            "response": "",
            "message": "Please report what you got",
            "shouldGo": "card1.html?cardID=" + str(lastGot)
        })
    card = models.Cards.objects.filter(cardID=cardID)
    if not len(card):
        return JsonResponse({
            "response": "",
            "message": "The cardID is unavailable"
        })
    user.update(lastGot=0)
    shareBy = models.User.objects.filter(username=card.shareBy)
    shareBy.update(cannotUseTimes=shareBy.first().cannotUseTime + 1)
    got = models.Got.objects.filter(gotCardID=cardID, gotBy=username)
    got.update(state=2)
    if got.first().th == 1:
        card.update(get1=2)
    elif got.first().th == 2:
        card.update(get2=2)
    else:
        card.update(get3=2)
    # card.update({  # removed kwargs=
    #     f"get{got.first().th}": 2
    # })
    return JsonResponse({
        "response": "ok"
    })

