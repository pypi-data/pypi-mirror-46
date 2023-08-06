from ucenter.http_handler.user.login.with_pwd import PwdLogging
from tornado import gen
import json
from ucenter.services.async_wrap import ctrl_user
import os
from tweb import tools
from ucenter.services import uid
from tweb.error_exception import ErrException, ERROR


class RegisterHandling(PwdLogging):

    @gen.coroutine
    def post(self):
        if self.is_api_mode():
            ret = yield self._post_api()
            return self.write(ret)
        else:
            next_url = yield self._post_web()
            self.redirect(next_url)

    @gen.coroutine
    def _post_api(self):
        data = json.loads(self.request.body.decode('utf-8'))
        user_id = data.get('id')
        name = data.get('name').lower()
        nickname = data.get('nickname')
        pwdh = data.get('pwd_hash')

        if user_id is None:
            raise ErrException(ERROR.E40005)

        # 注册时保证 user_id 由服务端生成，十分钟有效
        valid = yield uid.verify_user_id(user_id)
        if not valid:
            raise ErrException(ERROR.E40104)
        if name is None:
            raise ErrException(ERROR.E40001)
        if pwdh is None:
            raise ErrException(ERROR.E40006)

        salt = os.urandom(12).hex()
        pwd_hash = tools.gen_sha256(pwdh + salt)

        # 添加用户
        yield ctrl_user.add({
            'id': user_id,
            'name': name,
            'nickname': nickname,
            'salt': salt,
            'pwd_hash': pwd_hash})

        (user, token) = yield self._gen_token(user_id, pwdh)
        if token is None:
            raise ErrException(ERROR.E40102)

        return {'access_token': token, 'user': user}

    @gen.coroutine
    def _post_web(self):
        name = self.get_argument("name", None)
        pwd = self.get_argument("password", None)

        user_id = yield uid.gen_user_id()

        pwdh = tools.gen_sha256(user_id + pwd)

        salt = os.urandom(12).hex()
        pwd_hash = tools.gen_sha256(pwdh + salt)

        # 添加用户
        yield ctrl_user.add({'id': user_id, 'name': name.lower(), 'salt': salt, 'pwd_hash': pwd_hash})

        (user, token) = yield self._gen_token(user_id, pwd_hash)
        if token is None:
            return self.redirect(self.get_login_url())

        self.set_secure_cookie("user-id", user_id)
        self.set_secure_cookie("access-token", token)

        return self.get_argument("next", '/')
