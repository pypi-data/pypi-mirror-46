# coding=utf-8

import config
from mcenter.http_handler import msg_tpl_handler


base = '{}/{}/mc'.format(config.VER, config.PLATFORM)
routes = [
    # 消息模板增删改查
    (r"/%s/tpl/(\w+)" % base, msg_tpl_handler.MsgTplHandler),
]
