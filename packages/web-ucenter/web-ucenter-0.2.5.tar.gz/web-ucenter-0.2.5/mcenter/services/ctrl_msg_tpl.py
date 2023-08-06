# coding:utf-8

from tweb.error_exception import ErrException, ERROR
from mcenter.db import mongo as db
from tweb import time


def add(name, data):
    if 'content' not in data:
        raise ErrException(ERROR.E40000, extra='need content field')

    temp = {
        'name': name,
        'content': data['content']
    }
    if 'title' in data:
        temp['title'] = data['title']
    if 'greetings' in data:
        temp['greetings'] = data['greetings']
    if 'sender' in data:
        temp['sender'] = data['sender']
    if 'ps' in data:
        temp['ps'] = data['ps']

    now = time.millisecond()
    temp['created'] = now
    temp['updated'] = now
    db.msg_tpl.insert_one(temp)
    return get(name)


def get(name):

    tpl = db.msg_tpl.find_one({'name': name}, {'_id': 0, 'name': 0, 'created': 0, 'updated': 0})
    if tpl is None:
        raise ErrException(ERROR.E40400)

    return tpl
