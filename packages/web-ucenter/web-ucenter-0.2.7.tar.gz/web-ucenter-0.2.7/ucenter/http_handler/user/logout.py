from tweb import base_handler
from tweb import access_token
from tornado import gen


class LogoutHandling(base_handler.BaseHandler):

    @gen.coroutine
    def get(self):
        if self.is_api_mode():
            # API模式
            user_id = self.request.headers.get("x-user-id")
            x_access_token = self.request.headers.get("x-access-token")

            yield access_token.remove_access_token(user_id, x_access_token)

            self.write({})

        else:
            # 网页模式
            user_id = self.get_secure_cookie("user-id")
            x_access_token = self.get_secure_cookie("access-token")

            self.set_secure_cookie("access-token", '', expires_days=0)
            self.set_secure_cookie("user-id", '', expires_days=0)

            if user_id is None:
                return None
            if x_access_token is None:
                return None

            user_id = user_id.decode()
            x_access_token = x_access_token.decode()

            yield access_token.remove_access_token(user_id, x_access_token)

            self.redirect('/')

    def post(self):
        return self.get()
