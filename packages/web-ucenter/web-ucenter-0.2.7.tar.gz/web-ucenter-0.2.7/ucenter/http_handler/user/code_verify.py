from tweb import base_handler
from tornado import gen
from ucenter.services import verify_code, ctrl_user
import json
from ucenter.services.permit import gen_permit


class CodeVerify(base_handler.BaseHandler):

    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        code_token = data.get('code_token')
        code = data.get('code')

        # 校验验证码，同时取出记录信息
        record = yield verify_code.verify_code(code_token, code)
        indicator = record.get('indicator')
        permit_ret = yield gen_permit(indicator, 300)

        _id = ''
        user = ctrl_user.get(indicator)
        if user is not None:
            _id = user.get('id')

        ret = {
            'id': _id,
            'indicator': indicator,
            'permit': permit_ret.get('permit')
        }

        self.write(ret)
