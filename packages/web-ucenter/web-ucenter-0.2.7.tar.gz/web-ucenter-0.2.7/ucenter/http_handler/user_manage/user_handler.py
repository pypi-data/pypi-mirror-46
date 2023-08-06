from tornado import gen
from ucenter.services.async_wrap import ctrl_user
from tweb import myweb, base_handler


# 用户列表
class UsersHandler(base_handler.BaseHandler):

    @gen.coroutine
    def get(self):
        ret = yield ctrl_user.list_all()
        result = {
            'list': ret
        }
        return self.write(result)


# 用户信息
class UserHandler(base_handler.BaseHandler):

    # 读取
    @myweb.authenticated
    @gen.coroutine
    def get(self, *args, **kwargs):
        indicator = args[0]
        ret = yield ctrl_user.get(indicator)
        return self.write(ret)
