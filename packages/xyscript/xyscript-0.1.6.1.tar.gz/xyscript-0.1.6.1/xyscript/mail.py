#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr,formataddr
import xyscript.globalvar as gv

mail_host = "smtp.163.com"  # 设置服务器
mail_user = "idouko@163.com"  # 用户名
mail_pass = "XYCoder02"  # 三方邮箱口令
sender = 'idouko@163.com'# 发送者邮箱
receivers = ['m18221031340@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

class Email():
    def __init__(self,receiver):
        global receivers
        if len(receiver) > 0:
            receivers = receiver
            print (receivers)
        print(receivers)

    def send_package_email(self):
        pass

    def sendemail(self, content ,cc=None ,type=None, file=None):
        global receivers
        versionDsc = content
        subject = '此邮件来自自动化打包'#邮件来源
        message = MIMEText(versionDsc, 'plain', 'utf-8')

        message['From'] = formataddr(["iOS开发组", sender])
        message['To'] = ";".join(receivers)
        message['Subject'] = Header(subject, 'utf-8')#编码方式
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件" + str(e))

if __name__ == "__main__":
    Email([]).sendemail('您好！有新的IPA包可以下载，下载地址...\nhttps://www.baidu.com')