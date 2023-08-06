from tweb import base_handler
from tornado import gen
from ucenter.services.async_wrap import ctrl_user
from ucenter.services import user_indicate, uid


class UserIdentifying(base_handler.BaseHandler):
    @gen.coroutine
    def get(self):
        indicator = self.get_argument('indicator')
        indicator = indicator.lower()

        user = yield ctrl_user.get(indicator)

        user_id = None
        if user is not None:
            user_id = user.get('id')
        else:
            user = dict()
            if user_indicate.is_username(indicator):
                user_id = yield uid.gen_user_id()

        fields = dict()
        fields['name'] = 1 if user.get('name') else 0
        fields['pwd'] = 1 if user.get('has_pwd') else 0
        fields['email'] = 1 if user.get('email') else 0
        fields['mobile'] = 1 if user.get('mobile') else 0
        fields['weixin'] = 1 if user.get('weixin') else 0

        result = {'fields': fields}
        if user_id is not None:
            result['id'] = user_id
        self.write(result)
