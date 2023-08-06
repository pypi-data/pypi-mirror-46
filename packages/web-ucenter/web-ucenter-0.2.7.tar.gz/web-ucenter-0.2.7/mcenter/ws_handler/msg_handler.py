import config
from tornado.websocket import WebSocketHandler
from ..channels import ws
import logging
from tweb import access_token
from tornado import gen

whitelist = config.MC['origins']['whitelist']
blacklist = config.MC['origins']['blacklist']


class MessageHandler(WebSocketHandler):

    def check_origin(self, origin):
        if origin not in whitelist:
            logging.warning('%s not in white list' % origin)
            return False
        if origin in blacklist:
            logging.warning('%s is in black list' % origin)
            return False
        return True

    def data_received(self, chunk):
        pass

    @gen.coroutine
    def open(self):

        uid = self.get_argument('uid', None)
        token = self.get_argument('token', None)
        remote_ip = self.request.remote_ip
        valid = yield access_token.verify_access_token(uid, token, remote_ip)
        if valid:
            ws.add_channel(self, uid=uid, access_token=token, remote_ip=remote_ip)
        else:
            ws.add_channel(self)

    def on_close(self):
        ws.remove_channel(self)

    def on_message(self, message):
        if message.upper() == 'PING':
            self.write_message('PONG')
