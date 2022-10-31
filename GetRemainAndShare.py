'''
Author: LetMeFly
Date: 2022-10-31 14:04:44
LastEditors: LetMeFly
LastEditTime: 2022-10-31 14:12:05
'''
import requests

response = requests.get("https://back.share1024.letmefly.xyz/card/remain/typeAndID/")
remain = """
# 大家有卡牌可以分享到这里

https://share1024.letmefly.xyz/

这里也可以查看剩余卡牌的类型、张数

# 赠人玫瑰，手留余香 :）

领取之后再分享回来就可以了

# 剩余卡牌

"""

cards = response.json()

for cardID in cards:
    remain += f"+ 分享卡牌“{cards[cardID]}”：https://share1024.letmefly.xyz/card1.html?cardID={cardID}\n"

print(remain)

try:
    import pyperclip
    pyperclip.copy(remain)
    print("内容已复制，快去分享吧！")
except:
    pass
