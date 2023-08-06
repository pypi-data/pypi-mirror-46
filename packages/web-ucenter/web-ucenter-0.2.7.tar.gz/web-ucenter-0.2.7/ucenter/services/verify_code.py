#!/usr/bin/python
# coding:utf-8

import config
from tweb.error_exception import ErrException, ERROR
from tweb import tools
import random
from tweb import rdpool
import json

max_valid_time = config.Code['max_valid_time']
re_apply_interval = config.Code['re_apply_interval']


def gen_code(way_type, indicator):
    """
    :param way_type: 接收方式，eg. sms, email
    :param indicator: 手机号码或者email地址
    :return: (code, {'code_token': 'xxxxxx', 'timeout': timeout})
    """
    indicator = indicator.lower()

    ttl = rdpool.rds.ttl(_key_limit(indicator))
    if ttl is not None and ttl > 0:
        raise ErrException(ERROR.E40304, extra='Please retry after {} seconds'.format(ttl))

    code_token = tools.gen_id3()
    code = random.randint(100000, 999999)

    rdpool.rds.set(_key(code_token, code), json.dumps({'type': way_type, 'indicator': indicator}), max_valid_time)

    ret = {'code_token': code_token, 'timeout': re_apply_interval}

    # 记录该号码或者地址上次发送信息，用以防止频繁发送
    rdpool.rds.set(_key_limit(indicator), ret, re_apply_interval)

    return code, ret


async def verify_code(code_token, code):
    key = _key(code_token, code)
    data = rdpool.rds.get(key)
    if data is None:
        raise ErrException(ERROR.E40103)

    rdpool.rds.delete(key)
    record = json.loads(data)
    return record


def _key(code_token, code):
    return '{}/user/code/{}/{}'.format(config.PLATFORM, code_token, code)


def _key_limit(indicator):
    return '{}/user/code/limit/{}'.format(config.PLATFORM, indicator)
