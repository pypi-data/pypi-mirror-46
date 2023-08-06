#!/usr/bin/python
# coding:utf-8

from config import MongoServer
import pymongo

MongoCfg = {
    'authSource': 'mcdb',
    'username': 'app',
    'password': 'Mc2app',
    'connecttimeoutms': 60 * 1000
}

mongo_client = None
mongo_db = None

msg_tpl = None


def init():
    if not MongoServer['active']:
        return

    global mongo_client
    global mongo_db

    global msg_tpl

    if mongo_client is not None:
        return

    server = MongoServer['mongodb'].split(':')
    host = server[0]
    port = int(server[1]) if len(server) > 1 else 27017

    mongo_client = pymongo.MongoClient(host=host, port=port, **MongoCfg)
    mongo_db = mongo_client[MongoCfg['authSource']]

    # collections
    msg_tpl = mongo_db.msg_tpl

    # 创建索引
    _msg_tpl_index()


def start_session():
    return mongo_client.start_session()


def _msg_tpl_index():
    """ message templates sample
    {
        "_id": ObjectId("5c393f37e155ac54355b37ef"), # 用户ID，使用ObjectId
        "name": "verify_code_001",                   # 模板名称
        "status": 1,                                 # 0: 锁定，1: 正常
        'title': '标题',
        'greetings': '问候',
        'content': '内容',
        'sender': '发送者落款',
        'ps': '附加信息，如公司官网地址'
        "created": 1546763523000,                    # 毫秒
        "updated": 1546763523000,                    # 毫秒
    }
    """

    msg_tpl.create_index('name', unique=True)
