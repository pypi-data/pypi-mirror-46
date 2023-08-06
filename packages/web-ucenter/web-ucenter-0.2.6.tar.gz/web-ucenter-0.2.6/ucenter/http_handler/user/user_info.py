from tweb import base_handler
from tornado import gen
from ucenter.services.async_wrap import ctrl_user
from tweb import myweb


# 获取登录用户的信息
class UserInfoGetting(base_handler.BaseHandler):

    # 读取
    @myweb.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        user_id = self.request.headers.get('x-user-id')
        ret = yield ctrl_user.get(user_id)
        return self.write(ret)
