from tweb import base_handler
from tornado import gen
from tweb import myweb
import json
from ..services.async_wrap import ctrl_msg_tpl


class MsgTplHandler(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def post(self, name):
        data = json.loads(self.request.body.decode('utf-8'))

        ret = yield ctrl_msg_tpl.add(name, data)

        self.write(ret)

    @myweb.authenticated
    @gen.coroutine
    def get(self, name):
        ret = yield ctrl_msg_tpl.get(name)

        self.write(ret)
