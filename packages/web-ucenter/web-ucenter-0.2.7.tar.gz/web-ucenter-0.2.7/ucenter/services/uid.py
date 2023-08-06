#!/usr/bin/python
# coding:utf-8

import config
from tweb import rdpool
import json
from bson.objectid import ObjectId


async def gen_user_id():
    temp_id = ObjectId().__str__()

    record = ''
    key = _key(temp_id)
    rdpool.rds.set(key, json.dumps(record), 600)

    return temp_id


async def verify_user_id(user_id):
    key = _key(user_id)
    data = rdpool.rds.get(key)
    if data is not None:
        rdpool.rds.delete(key)
    return data is not None


def _key(user_id):
    return '{}/user/gen/id/{}'.format(config.PLATFORM, user_id)
