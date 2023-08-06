import json
import os

from ucenter.services.async_wrap import ctrl_user
from tweb import base_handler
from tweb import myweb
from tweb.error_exception import ErrException, ERROR
from tweb import tools, access_token
from tornado import gen

from ucenter.services.permit import verify_permit


class PasswordSetting(base_handler.BaseHandler):
    @myweb.authenticated
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        user_id = self.request.headers.get("x-user-id")
        pwdh = data.get('pwd_hash')
        old_pwdh = data.get('old_pwd_hash')

        if user_id is None:
            raise ErrException(ERROR.E40005)
        if pwdh is None:
            raise ErrException(ERROR.E40006)

        user = yield ctrl_user.get(user_id, unsafely=True)
        if user.get('pwd_hash') is not None:
            if old_pwdh is None:
                raise ErrException(ERROR.E40102)
            # 用户存在密码时，校验旧密码
            salt = user.get('salt')
            temp = tools.gen_sha256(old_pwdh + salt)
            pwdhs = user.get('pwd_hash')
            if temp != pwdhs:
                raise ErrException(ERROR.E40102)

        salt = os.urandom(12).hex()
        pwd_hash = tools.gen_sha256(pwdh + salt)

        user = yield ctrl_user.set_pwd({
            'user_id': user_id,
            'pwd_hash': pwd_hash,
            'salt': salt
        })

        # 移除所有该用户的token，使已登陆用户无效
        yield access_token.remove_access_token(user_id, '*')

        token = yield access_token.gen_access_token(user_id, self.request.remote_ip)
        return self.write({'access_token': token, 'user': user})


class PasswordResetting(base_handler.BaseHandler):
    @gen.coroutine
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        indicator = data.get('indicator')
        permit = data.get('permit')
        pwdh = data.get('pwd_hash')

        yield verify_permit(indicator, permit)

        user = yield ctrl_user.get(indicator)

        if user is None:
            raise ErrException(ERROR.E40101)

        salt = os.urandom(12).hex()
        pwd_hash = tools.gen_sha256(pwdh + salt)

        user_id = user.get('id')
        yield ctrl_user.set_pwd({
            'user_id': user_id,
            'pwd_hash': pwd_hash,
            'salt': salt
        })

        # 移除所有该用户的token，使已登陆用户无效
        yield access_token.remove_access_token(user_id, '*')
        return self.write({'indicator': indicator})
