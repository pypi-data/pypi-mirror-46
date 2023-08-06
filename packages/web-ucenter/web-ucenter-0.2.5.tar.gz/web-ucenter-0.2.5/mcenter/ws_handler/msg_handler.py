from tornado.websocket import WebSocketHandler
from ..channels import ws
import logging
from tweb import access_token
from tornado import gen


class MessageHandler(WebSocketHandler):

    def check_origin(self, origin):
        # TODO: 需要检查同源请求
        logging.info('websocket client from %s' % origin)
        return True

    def data_received(self, chunk):
        pass

    @gen.coroutine
    def open(self):

        uid = self.request.headers.get('x-user-id')
        token = self.request.headers.get('x-access-token')
        remote_ip = self.request.remote_ip
        valid = yield access_token.verify_access_token(uid, token, remote_ip)
        if not valid:
            self.close(code=4031, reason='invalid access token')
            logging.error('invalid access token, from %s' % remote_ip)

        if uid is not None:
            ws.add_user_channel(uid, self)
        else:
            self.close(code=4032, reason='no uid')
            logging.error('no uid, from %s' % remote_ip)

    def on_close(self):
        uid = self.request.headers.get('x-user-id')
        if uid is not None:
            ws.remove_user_channel(uid)

    def on_message(self, message):
        pass

