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
