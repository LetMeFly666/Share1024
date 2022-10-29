'''
Author: LetMeFly
Date: 2022-10-28 14:22:43
LastEditors: LetMeFly
LastEditTime: 2022-10-29 12:37:20
'''
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
from Secrets import EMAIL_SENDER_NAME, EMAIL_SENDER_PASSWORD


def sendEmail(toWho="Tisfy@qq.com", title="Share1024 验证码", text="力扣1024卡牌分享网 欢迎您"):
    my_sender = EMAIL_SENDER_NAME  # 发件人邮箱账号
    my_pass = EMAIL_SENDER_PASSWORD  # 发件人邮箱密码
    my_user = toWho  # 收件人邮箱账号，我这边发送给自己

    def mail():
        ret = True
        try:
            msg = MIMEText(text, 'plain', 'utf-8')
            msg['From'] = formataddr(["LetMeFly", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["Hello", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = title  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except smtplib.SMTPRecipientsRefused:
            print("地址错误")
            ret = False
        except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print(e)
            ret = False
        '''
         raise SMTPRecipientsRefused(senderrs)
smtplib.SMTPRecipientsRefused: {'': (501, b'Bad address syntax. http://service.mail.qq.com/cgi-bin/help?subtype=1&&id=20022&&no=1000730')}
        '''
        return ret

    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
    return ret


def sendEmail_html(to_who_list=["Tisfy@qq.com"], title="Share1024", html="<font color='red'>力扣1024卡牌分享网注册</font>"):
    my_sender = EMAIL_SENDER_NAME
    my_pass = EMAIL_SENDER_PASSWORD
    receivers = to_who_list  # 接收邮件

    message = MIMEText(html, 'html', 'utf-8')
    message['From'] = Header("LetMeFly", 'utf-8')
    message['To'] = Header("你好", 'utf-8')
    message['Subject'] = Header(title, 'utf-8')

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == "__main__":
    sendEmail_html()
