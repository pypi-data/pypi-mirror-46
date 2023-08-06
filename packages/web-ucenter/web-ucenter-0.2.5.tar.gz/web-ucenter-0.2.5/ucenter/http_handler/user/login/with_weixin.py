import json

from ucenter.services.async_wrap import ctrl_user
from tweb import base_handler, access_token
from tornado import gen

from ucenter.services.weixin import wx_utils
from tweb.error_exception import ErrException, ERROR
from ucenter.services import uid


class WeixinLogging(base_handler.BaseHandler):
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        code = data.get('code')
        platform = 'weixin'

        if code is None:
            raise ErrException(ERROR.E40008)

        token_dict = yield wx_utils.get_access_token_async(code)
        token = token_dict['access_token']
        open_id = token_dict['openid']

        user_info = yield wx_utils.get_user_info_async(token, open_id)

        oauth = {
            'open_id': open_id,
            'union_id': user_info.get('unionid'),
            'nickname': user_info.get('nickname'),
            'icon': user_info.get('headimgurl')
        }
        if oauth['union_id'] is None:
            oauth.pop('union_id')

        user = yield ctrl_user.get_with_open_id(platform, open_id)
        if user is None:
            # 用户不存在，创建用户
            user_id = yield uid.gen_user_id()
            user = yield ctrl_user.add({
                'id': user_id,
                'nickname': user_info.get('nickname'),
                'gender': user_info.get('sex'),
                'country': user_info.get('country'),
                'province': user_info.get('province'),
                'city': user_info.get('city'),
                'icon': user_info.get('headimgurl'),
                platform: oauth
            })
        else:
            # 保存最新的微信用户信息
            user = yield ctrl_user.update_oauth(platform, oauth)

        user_id = user.get('id')
        token = yield access_token.gen_access_token(user_id, self.request.remote_ip)
        return self.write({'access_token': token, 'user': user})
