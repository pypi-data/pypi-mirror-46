from tweb import base_handler, access_token
import json
from tornado.httpclient import AsyncHTTPClient
from Crypto.Cipher import AES
import base64
from tornado import gen
from ucenter.services.async_wrap import ctrl_user
from tweb.error_exception import ErrException, ERROR
from ucenter.services import uid

app_id = 'wx91d688d6712f9222'
secret = 'b90c5949bf56c0416a3a8fe78d65ed36'


class WxmpLogging(base_handler.BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body.decode('utf-8'))
        code = data.get('code')
        encrypted_data = base64.b64decode(data.get('encryptedData'))
        iv = base64.b64decode(data.get('iv'))

        platform = 'wxmp'

        if code is None:
            raise ErrException(ERROR.E40008)

        user_info = yield get_user_info(code, iv, encrypted_data)
        open_id = user_info.get('openId')
        oauth = {
            'open_id': open_id,
            'union_id': user_info.get('unionId'),
            'nickname': user_info.get('nickName'),
            'icon': user_info.get('avatarUrl')
        }
        if oauth.get('union_id') is None:
            oauth.pop('union_id')

        user = yield ctrl_user.get_with_open_id(platform, open_id)
        if user is None:
            # 用户不存在，创建用户

            user_id = yield uid.gen_user_id()

            user = yield ctrl_user.add({
                'id': user_id,
                'nickname': user_info.get('nickName'),
                'gender': user_info.get('gender'),
                'country': user_info.get('country'),
                'province': user_info.get('province'),
                'city': user_info.get('city'),
                'icon': user_info.get('avatarUrl'),
                platform: oauth
            })
        else:
            # 保存最新的微信用户信息
            user = yield ctrl_user.update_oauth(platform, oauth)

        user_id = user.get('id')
        token = yield access_token.gen_access_token(user_id, self.request.remote_ip)

        return self.write({'access_token': token, 'user': user})


async def get_user_info(code, iv, encrypted_data):
    url = 'https://api.weixin.qq.com/sns/jscode2session?' \
          'appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(app_id, secret, code)

    response = await AsyncHTTPClient().fetch(url)
    obj = json.loads(response.body.decode('utf-8'))
    session_key = base64.b64decode(obj.get('session_key'))
    print('from jscode2session: %s' % obj)

    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    wx_user_info = json.loads(cipher.decrypt(encrypted_data).decode('utf-8'))
    wx_user_info['unionId'] = obj.get('unionid')
    print('from encrypted_data: %s' % wx_user_info)

    return wx_user_info
