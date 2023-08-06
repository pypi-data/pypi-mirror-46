import json

from ucenter.services.async_wrap import ctrl_user
from tweb import base_handler
from tweb import myweb
from tornado import gen


class CommonUpdating(base_handler.BaseHandler):

    @myweb.authenticated
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        user_id = self.request.headers.get("x-user-id")
        user = yield ctrl_user.update(user_id, data)
        self.write({'user': user})
