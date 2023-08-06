from tweb.error_exception import ErrException, ERROR
from ucenter.services import ctrl_user
from ..channels import email, sms_5c as sms, ws
from ucenter.services.user_indicate import is_email, is_mobile


def send_with_uid(uid, msg, *args):
    """
    发送消息到指定用户绑定的邮箱或者手机号
    :param uid: 用户 id
    :param msg: {
        'title': '标题',
        'greetings': '问候',
        'content': '内容',
        'sender': '发送者落款',
        'ps': '附加信息，如公司官网地址'
    }
    :param args: options: "email", "sms", "ws, 单选或者多选
    :return:
    """
    user = ctrl_user.get(uid)

    if user is None:
        raise ErrException(ERROR.E40101)

    if 'sms' in args:
        mobile = user.get('mobile')
        if mobile is not None:
            sms.send_msg(mobile, msg)

    if 'email' in args:
        e_mail = user.get('email')
        if email is not None:
            email.send_msg(e_mail, msg)

    if 'ws' in args:
        ws.send_msg(uid, msg)


def send_directly(indicator, msg):
    """
    发送消息到邮箱或者手机号（短信），根据标示自动匹配
    :param indicator: 邮箱地址，或者手机号（国家码-号码）
    :param msg: {
        'title': '标题',
        'greetings': '问候',
        'content': '内容',
        'sender': '发送者落款',
        'ps': '附加信息，如公司官网地址'
    }
    :param args: options: "email", "sms", 单选或者多选
    :return:
    """

    if is_mobile(indicator):
        mobile = indicator
        sms.send_msg(mobile, msg)
    elif is_email(indicator):
        e_mail = indicator
        email.send_msg(e_mail, msg)
    else:
        raise ErrException(ERROR.E40000, extra='invalid indicator - %s' % indicator)
