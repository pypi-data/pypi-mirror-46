# coding=utf-8
import config
from ..ws_handler.msg_handler import MessageHandler

base = 'v1/{}/mc'.format(config.PLATFORM)
routes = [
    (r'/%s/message' % base, MessageHandler)
]
