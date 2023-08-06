# coding=utf-8

import mcenter
from .db import mongo
from . import routes


def init(app, load_routes=True):
    # 初始化消息中心
    mcenter.init(app, True)

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    if load_routes:
        app.load_routes(routes)
