from tornado import gen

from ucenter.services.async_wrap import ctrl_user
from tweb import base_handler
from tweb import myweb


class WeixinUnBinding(base_handler.BaseHandler):
    @myweb.authenticated
    @gen.coroutine
    def post(self):
        user_id = self.request.headers.get('x-user-id')

        user = yield ctrl_user.unbind_oauth(user_id, 'weixin')

        self.write({'user': user})
