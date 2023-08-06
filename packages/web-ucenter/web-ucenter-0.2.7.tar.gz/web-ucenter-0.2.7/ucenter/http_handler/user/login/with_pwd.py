import json
from tweb import base_handler
from tornado import gen
from ucenter.services.async_wrap import ctrl_user
from ucenter import services
from tornado.web import HTTPError
from tweb import tools, access_token
from tweb.error_exception import ErrException, ERROR


class PwdLogging(base_handler.BaseHandler):
    def get(self):
        next_url = self.get_argument("next", '/')
        action_url = '{}?next={}'.format(self.get_login_url(), next_url)
        self.render('login.html', action_url=action_url)

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
        pwd_hash = data.get('pwd_hash')

        (user, token) = yield self._gen_token(user_id, pwd_hash)
        if token is None:
            raise ErrException(ERROR.E40102)

        return {'access_token': token, 'user': user}

    @gen.coroutine
    def _post_web(self):
        name = self.get_argument("name", None)
        pwd = self.get_argument("password", None)

        user = yield ctrl_user.get(name)
        if user is None:
            raise HTTPError(403, 'user not existed: %s' % name)

        user_id = user.get('id')
        pwd_hash = tools.gen_sha256(user_id + pwd)

        try:
            (user, token) = yield self._gen_token(user_id, pwd_hash)
        except ErrException as e:
            raise HTTPError(403, '%s' % e.err.message())

        if token is None:
            return self.redirect(self.get_login_url())

        self.set_secure_cookie("user-id", user_id)
        self.set_secure_cookie("access-token", token)

        return self.get_argument("next", '/')

    @gen.coroutine
    def _gen_token(self, user_id, pwd_hash):
        user = yield ctrl_user.get(user_id, unsafely=True)

        if user is None:
            raise ErrException(ERROR.E40101)

        salt = user.get('salt')
        temp = tools.gen_sha256(pwd_hash + salt)

        pwdhs = user.get('pwd_hash')

        if pwdhs == temp:
            token = yield access_token.gen_access_token(user_id, self.request.remote_ip)
            return services.ctrl_user.out_filter(user), token
        else:
            raise ErrException(ERROR.E40102)
