from tweb.error_exception import ErrException, ERROR
from tweb import base_handler
from ucenter.services.verify_code import gen_code
from ucenter.services.user_indicate import is_email, is_mobile
from tornado import gen
from mcenter.services.async_wrap import messenger, ctrl_msg_tpl


class SendCodeGenerating(base_handler.BaseHandler):
    @gen.coroutine
    def get(self):
        indicator = self.get_argument('indicator')

        if is_email(indicator):
            way = 'email'
        elif is_mobile(indicator):
            way = 'mobile'
        else:
            raise ErrException(ERROR.E40000, extra='wrong indicator - %s' % indicator)

        (code, ret) = gen_code(way, indicator)

        params = {'code': code}

        msg = yield ctrl_msg_tpl.get('code')
        msg['content'] = msg['content'].format(**params)
        yield messenger.send_directly(indicator, msg)

        self.write(ret)
