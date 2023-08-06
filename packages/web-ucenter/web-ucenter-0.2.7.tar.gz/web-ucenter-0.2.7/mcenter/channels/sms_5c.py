import hashlib
from tweb.error_exception import ErrException, ERROR
import urllib.parse
import urllib.request

from ucenter.services import user_indicate

# 第三方短信服务
sms_url = 'http://m.5c.com.cn/api/send/index.php'
sms_apikey = 'd4b4078228dc52dab84e6bbc93705f1e'
sms_username = 'njbhwl'
sms_password = 'asdf1234'
sms_password_md5 = hashlib.md5(sms_password.encode('utf-8')).hexdigest()


def send_msg(mobile, msg):
    """
    发送短信
    :param mobile: 手机号码，字符串，格式：国家吗-号码
    :param msg: {
        'title': '标题',
        'greetings': '问候',
        'content': '内容',
        'sender': '发送者落款',
        'ps': '附加信息，如公司官网地址'
    }
    """
    if not user_indicate.is_mobile(mobile):
        raise ErrException(ERROR.E40003)

    mst_array = list()
    if 'title' in msg:
        mst_array.append(msg['title'])
    if 'content' in msg:
        mst_array.append(msg['content'])
    # if 'sender' in msg:
    #     mst_array.append(msg['sender'])
    # if 'ps' in msg:
    #     mst_array.append(msg['ps'])

    msg_text = ' - '.join(mst_array)

    mobile = mobile.replace('-', '')
    values = {
        'username': sms_username,
        'password_md5': sms_password_md5,
        'apikey': sms_apikey,
        'mobile': mobile,
        'content': msg_text,
        'encode': 'UTF-8'
    }

    try:
        data = urllib.parse.urlencode(values)
        req = urllib.request.Request(sms_url + '?' + data)
        response = urllib.request.urlopen(req)
        res = response.read().decode('utf-8')
    except Exception as e:
        raise ErrException(ERROR.E50002, e=e)

    if 'success' not in res:
        error = res.split(':')[1]
        raise ErrException(ERROR.E50002, 'error in send sms: %s' % error)
