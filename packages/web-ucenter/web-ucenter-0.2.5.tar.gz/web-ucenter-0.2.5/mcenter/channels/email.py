#!/usr/bin/python
# coding:utf-8
from config import EMAIL
import logging
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from tweb.error_exception import ErrException, ERROR
from ucenter.services import user_indicate

# 第三方 SMTP 服务
_mail_host = EMAIL['mail_host']
_mail_user = EMAIL['mail_user']
_mail_pass = EMAIL['mail_pass']
_mail_nick = EMAIL['main_nick']


def send_msg(email, msg):
    """
    发送邮件
    :param email: 接收邮件的邮箱地址
    :param msg: {
        'title': '标题',
        'greetings': '问候',
        'content': '内容',
        'sender': '发送者落款',
        'ps': '附加信息，如公司官网地址'
    }
    """
    if not user_indicate.is_email(email):
        raise ErrException(ERROR.E40003)
    try:
        smtp = smtplib.SMTP_SSL(_mail_host, 465, keyfile=EMAIL['cert_key'], certfile=EMAIL['cert_pem'])
    except FileNotFoundError:
        logging.warning('not found %s or %s, will use port 25 to send email!' % (EMAIL['cert_key'], EMAIL['cert_pem']))
        smtp = smtplib.SMTP(_mail_host, 25)

    smtp.ehlo()
    smtp.login(_mail_user, _mail_pass)

    receivers = [email]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mst_array = list()
    if 'greetings' in msg:
        mst_array.append(msg['greetings'])
    if 'content' in msg:
        mst_array.append(msg['content'])
    if 'sender' in msg:
        mst_array.append(msg['sender'])
    if 'ps' in msg:
        mst_array.append(msg['ps'])

    msg_text = '\n\n'.join(mst_array)
    message = MIMEText(msg_text, 'plain', 'utf-8')
    # message['From'] = Header(_mail_user, 'utf-8')
    message['From'] = formataddr([_mail_nick, _mail_user])  # 发件人邮箱昵称、发件人邮箱账号
    message['To'] = Header(email, 'utf-8')
    message['Subject'] = Header(msg['title'], 'utf-8')

    try:
        smtp.sendmail(_mail_user, receivers, message.as_string())
    except smtplib.SMTPException as e:
        raise ErrException(ERROR.E50001, extra=e.args[0], e=e)
    finally:
        smtp.quit()
