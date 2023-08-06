import json

from tornado import gen

from ucenter.services.async_wrap import ctrl_user
from tweb import base_handler
from tweb import myweb
from tweb.error_exception import ErrException, ERROR
from ucenter.services import verify_code
from ucenter.services.permit import verify_permit


class CodeBinding(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))

        user_id = self.request.headers.get('x-user-id')

        code_token = data.get('code_token')
        code = data.get('code')

        # 校验验证码，同时取出记录信息
        record = yield verify_code.verify_code(code_token, code)

        id_type = record.get('type')
        indicator = record.get('indicator')

        temp = yield ctrl_user.get(indicator)
        if temp is not None:
            # 手机或邮箱已被注册
            raise ErrException(ERROR.E40302, extra=indicator)

        user = yield ctrl_user.get(user_id)

        if id_type in user:
            raise ErrException(ERROR.E40303, extra=id_type)

        user = yield ctrl_user.bind(user_id, id_type, indicator)

        self.write({'user': user})

    @myweb.authenticated
    @gen.coroutine
    def put(self):
        data = json.loads(self.request.body.decode('utf-8'))

        user_id = self.request.headers.get('x-user-id')

        # # 许可
        # permit = data.get('permit')
        # # 已绑定的手机号码或者邮箱
        # bind_indicator = data.get('indicator')

        code_token = data.get('code_token')
        code = data.get('code')

        # # 校验许可
        # yield verify_permit(bind_indicator, permit)

        # 校验验证码，同时取出记录信息
        record = yield verify_code.verify_code(code_token, code)

        # 新号码
        id_type = record.get('type')
        indicator = record.get('indicator')

        temp = yield ctrl_user.get(indicator)
        if temp is not None:
            # 手机或邮箱已被注册
            raise ErrException(ERROR.E40302, extra=indicator)

        user = yield ctrl_user.update_bind(user_id, id_type, indicator)
        self.write({'user': user})
