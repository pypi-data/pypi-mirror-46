from tweb import base_handler, access_token
from tornado import gen
from ucenter.services import verify_code, uid
import json
from ucenter.services.async_wrap import ctrl_user


class CodeLogging(base_handler.BaseHandler):

    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        code_token = data.get('code_token')
        code = data.get('code')

        # 校验验证码，同时取出记录信息
        record = yield verify_code.verify_code(code_token, code)

        id_type = record.get('type')
        indicator = record.get('indicator')

        user = yield ctrl_user.get(indicator)
        if user is None:
            # 注册新用户
            user_id = yield uid.gen_user_id()
            user = yield ctrl_user.add({'id': user_id, id_type: indicator})

        # 生成access token
        user_id = user.get('id')
        token = yield access_token.gen_access_token(user_id, self.request.remote_ip)

        self.write({'access_token': token, 'user': user})
