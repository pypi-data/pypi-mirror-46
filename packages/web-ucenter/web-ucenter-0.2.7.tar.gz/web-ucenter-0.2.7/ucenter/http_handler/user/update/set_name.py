import json

from ucenter.services.async_wrap import ctrl_user
from tweb import myweb, base_handler
from tweb.error_exception import ErrException, ERROR
from tornado import gen

from ucenter.services import user_indicate


class NameSetting(base_handler.BaseHandler):
    @myweb.authenticated
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        user_id = self.request.headers.get("x-user-id")
        name = data.get('name')
        if not user_indicate.is_username(name):
            raise ErrException(ERROR.E40007)

        user = yield ctrl_user.get(user_id)
        if user.get('name') is not None:
            # 用户存在用户名
            raise ErrException(ERROR.E40303)

        user = yield ctrl_user.set_name(user_id, name)
        self.write({'user': user})
