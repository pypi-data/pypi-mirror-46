# coding=utf-8

from .db import mongo
from . import routes

from .channels import ws


def init(app, load_routes=True):

    # 初始化本系统数据库
    mongo.init()

    # 加载路由模块
    if load_routes:
        app.load_routes(routes)
