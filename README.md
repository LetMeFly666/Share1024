# Share1024
[力扣2022-1024马尔科夫链活动](https://leetcode.cn/2022-1024)，卡牌分享网，**当前正在搭建中**，后端服务可能只会运行到活动结束

在这里，你可以领取任意你需要的卡牌，但是，你领取完别人的卡牌后**必须分享出来**。只有这样，才能实现卡牌的*可持续发展*

在这里，**诚信至上，白嫖达咩** だめ

此项目完全公益，**不盈利**

因此，还请各位大佬手下留情，不要攻击我的低配服务器哦~

## 文件结构说明

```/docs/``` 文件夹其实为**前端页面**，Github pages 的 deploy from branch 不支持(root)和/docs之外的文件夹的自动部署

```/back/``` 文件夹为后端代码，运行在我的服务器上

### back

**准备阶段：**

1. 拥有一台具有公网ip并且已备案的服务器
2. 服务器上配置好```Python```、```django```、```MySQL```（最好为这个项目单独创建一个用户，防止可能的漏洞导致其他数据库的数据泄露问题）
3. 配置好例如Nginx等服务，以便将来自外网的访问转交给此服务进行处理。

**配置阶段：**

你需要在```/back/```文件夹下自己创建一```Secrets.py```，用于配置各种密码、令牌等。

此文件需要包括：

```python
"""这个文件中的内容需要自己配置，打死也不要告诉他人哦"""
SECRET_KEY = "django-insecure-qs0quxd^b0a0#2+6cxv)qs)(f(fx=m9ri_5#ladh8x5)i#cgh+"
DATABASE_DBNAME = ''  # 数据库名称
DATABASE_USER = ''  # 数据库用户名
DATABASE_PASSWORD = ''  # 数据库密码
DATABASE_HOST = ''  # 数据库服务器IP
DATABASE_PORT = 3306  # 数据库端口
EMAIL_SENDER_NAME = "Tisfy@qq.com"  # 邮件发送者邮箱
EMAIL_SENDER_PASSWORD = "LeetCode2022-1024Share"  # 邮件发送者密码

```

**启动服务：**

首次启动服务需要执行命令：

```bash
python manage.py makemigrations
python manage.py migrate
```

之后仅需运行

```bash
python manage.py runserver
```

## 接口说明

以下说明了后端为前端提供的各种接口，我提供这些接口是为了方便用户写程序去调用（比如卡牌监控等），但是请注意调用频率，不要对服务器照成太大的压力。推荐频率：1次/秒（蒟蒻的服务器不抗揍）

### /user/baseInfo/

获取用户基本信息

**方法**

POST

**请求**

data

```json
{
    "warrant1024": "theWarrant484s48e4fs84e"
}
```

**返回**

若未登录：

```json
{"login": false}
```

若已登录：

```json
{
    "username": "tisfy",
    "cardNotShare": ""  // 是否有领取但为传递的卡牌。如果无，则为空；如果有，则为卡牌ID
}
```

### /user/cards/

获取用户卡牌信息

**方法**

GET

**请求**

data

```json
{
    "warrant1024": "theWarrant484s48e4fs84e"
}
```

**返回**

若未登录，则返回的各种卡牌都为空列表

若已登录，则返回

```json
{
    "shared": [123, 542],  // 所分享的卡牌ID
    "got": [120, 521],  // 所领取的卡牌ID
    "error": [542],  // 被报失效的卡牌
}
```

### /user/login/

**方法**

POST

**请求**

data

```json
{
    "username": "tisfy",
    "password": "LeetCode2022-1024Share"
}
```

**返回**

若登录成功

```json
{
    "warrant1024": "theWarrant484s48e4fs84e"
}
```

否则

```json
{
    "warrant1024": "",
    "message": "Username or password wrong"
}
```

其中，message当前支持：

+ 账号或密码为空：```There isn't a username or password in the request```
+ 账号或密码不正确：```Username or password wrong```
+ 该账号不存在：```No such user```

### /user/logout/

**方法**

POST

**请求**

data

```json
{
    "warrant1024": "theWarrant484s48e4fs84e"
}
```

**响应**

```json
{
    "response": "ok"
}
```

### /user/register/

**请求**

data

```json
{
    "username": "tisfy",
    "password": "LeetCode2022and1024Share",
    "email": "Tisfy@qq.com",
    "code": "1234",  // 邮箱验证码
}
```

**返回**

若注册成功

```json
{
    "warrant1024": "theWarrant484s48e4fs84e"
}
```

否则

```json
{
    "warrant1024": "",
    "message": "Verification Code unavailable"
}
```

其中，message当前支持：

+ 用户名不合法：```Username unavailable```
+ 邮箱不合法：```Email unavailable```
+ 密码不合法：```Password unavailable```
+ 验证码不正确：```Verification Code unavailable```

### /user/register/sendCode/

**方法**

POST

**请求**

data

```json
{
    "email": "Tisfy@qq.com"
}
```

**返回**

若成功

```json
{
    "response": "ok"
}
```

否则

```json
{
    "response": "",
    "message": "Request too fast"
}
```

其中，message当前支持：

+ 发送过于频繁：```Request too fast```
+ 邮件地址不合法：```Email unavailable```
+ 其他原因的邮件发送失败：```Email send failed```

### /card/remain/all/

获取有多少张未被领取完的卡牌

**方法**

GET

**返回**

返回所有卡牌的未被领取数量（一张卡牌最多算一次）

```json
{
    "0": 21,
    "1": 50,
    // ...
}
```

### /card/remain/oneType/?cardType={卡牌类型}

返回某（一）种卡牌的所有未被领取的卡牌的ID

注意，```&```在此处被编码为```AND```

**方法**

GET

**示例**

```
/card/remain/oneType?cardType=007
```

**返回**

```json
[125, 129, 510, 515]
```

### /card/oneCard/?cardID={卡牌ID}

返回某张卡牌的具体信息

**方法**

GET

**返回**

若获取成功

```json
{
    "cardID": 125,
    "cardType": "007",
    "shareBy": "tisfy",  // 分享者
    "get1": 1,  //    |- 0：待领取    
    "get2": 2,  // ---|  1：已领取
    "get3": 0,  //    |- 2：被报无效
    "gotTimes": 2,  // 也能由get123求得
    // 注意，这里不包含力扣的卡牌领取链接，白嫖达咩
}
```

若获取失败

```json
{
    "cardID": 0,
    "message": "Card doesn't exist"
}
```

其中，message当前支持：

+ 卡牌不存在：```Card doesn't exist```

### /card/oneCard/getURL/

领取一张卡牌

**方法**

POST

**请求**

data:

```json
{
    "cardID": 1221,
}
```

**返回**

正常：

```json
{
    "leetcodeURL": "https://leetcode.cn/2022-1024?id=1111111&userSlug=tisfy"
}
```

若未登录：返回 到登录界面的```redirect```

若登录且有未传递的卡牌：返回 到卡牌传递界面的```redirect```

若卡牌为空或不存在：返回```{"leetcodeURL": "", "message": "Card doesn't exist"}```

若卡牌被领完：返回```{"leetcodeURL": "", "message": "Too late, all cards were taken"}```

### /card/share/

分享一张卡牌（为判断传递卡牌和原始卡牌是否相同）

**方法**

POST

**请求**

```json
{
    "parent": "",  // 若为领取后的传递而不是直接分享，则parent为空串；否则parent为领取自的卡牌  // 若parent的ID不合法，则默认为直接分享
    "leetcodeURL": "https://leetcode.cn/2022-1024?id=1111111&userSlug=tisfy",  // 力扣卡牌分享链接
    "type": "007",  // 卡牌类型
    // "remain": "3"  // 这张卡牌还剩几张（默认为3），不提倡，要保证没有公开卡牌分享链接
}
```

**返回**

若成功：

```json
{
    "newCardID": 1024
}
```

若未登录：返回 到登录界面的```redirect```

若登录且有未传递的卡牌且未传递的卡牌不是这张卡牌：返回 到正确的卡牌传递界面的```redirect```

若力扣卡牌链接不合法：返回 ```{"newCardID": "", "message": "Not a right link"}```

若卡牌类型不存在：返回 ```{"newCardID": "", "message": "We don't have a cardType of this"}```

### /card/cannotUse/

报无效

**方法**

POST

**请求**

data

```json
{
    "cardID": 159
}
```

**响应**

若成功：

```json
{
    "response": "ok"
}
````

若未登录：返回 到登录界面的```redirect```

若登录且有为传递的卡牌且未传递的卡牌不是这张卡牌：返回 到正确的卡牌传递界面的```redirect```

若登录且无未传递的卡牌：返回```{"response": "", "message": "Sorry, you shouldn't report this card"}```

若被报卡牌不存在：返回```{"response": "", "message": "The cardID is unavailable"}```

## End

By the way，通过a.com的网页向b.a.com发送登录请求，b.a.com真的没有办法直接设置a.com的cookie吗？X_X 或者说，三级域名能设置二级域名的cookie吗
