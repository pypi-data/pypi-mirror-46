import json

from tornado import gen

from ucenter.services.async_wrap import ctrl_user
from tweb import base_handler
from tweb import myweb
from ucenter.services.weixin import wx_utils
from tweb.error_exception import ErrException, ERROR


class WeixinBinding(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def post(self):
        platform = 'weixin'

        data = json.loads(self.request.body.decode('utf-8'))
        user_id = self.request.headers.get('x-user-id')

        code = data.get('code')

        if code is None:
            raise ErrException(ERROR.E40008)

        token_dict = yield wx_utils.get_access_token_async(code)
        access_token = token_dict['access_token']
        open_id = token_dict['openid']

        user = yield ctrl_user.get(user_id)
        oauth = user.get(platform)
        if oauth is not None:
            # 该用户已绑定微信
            raise ErrException(ERROR.E40303, extra=oauth['nickname'])

        user_info = yield wx_utils.get_user_info_async(access_token, open_id)
        oauth = {
            'open_id': open_id,
            'union_id': user_info.get('unionid'),
            'nickname': user_info.get('nickname'),
            'icon': user_info.get('headimgurl'),
            'extend': json.dumps(user_info),
        }
        if oauth['union_id'] is None:
            oauth.pop('union_id')

        user = yield ctrl_user.bind_oauth(user_id, platform, oauth)

        return self.write({'user': user})
