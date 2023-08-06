#!/usr/bin/python
# coding:utf-8

import base64
import hmac
import json
import time
import datetime
from hashlib import sha1 as sha
from tweb import snowflake
import config
import oss2
import logging

callback_host = config.OSS['callback_host']
access_key_id = config.OSS['access_key_id']
access_key_secret = config.OSS['access_key_secret']
host = config.OSS['host']
bucket_name = config.OSS['bucket_name']

callback_obj = {
    'callbackUrl': '{}/{}/uc/upload'.format(callback_host, config.VER),
    'callbackBodyType': 'application/json',
    'callbackBody': '{'
                    '"bucket":${bucket},'
                    '"object":${object},'
                    '"size":${size},'
                    '"mimeType":${mimeType},'
                    '"imageInfo":${imageInfo},'
                    '"x.sid":${x:sid},'
                    '"x.uid":${x:uid},'
                    '"x.lon":${x:lon},'
                    '"x.lat":${x:lat},'
                    '"x.desc":${x:desc},'
                    '"x.stat":${x:stat}'
                    '}'
}

oss2.set_stream_logger('oss2', level=logging.WARNING)

auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, host, bucket_name, is_cname=True)


def get_policy(user_id, timeout):
    expire_time = int(time.time()) + timeout

    instance_id = config.Port * 100 + config.ID
    file_id = snowflake.Snowflake(instance_id).generate()

    path = '{}/{}/{}'.format('private', user_id, file_id)
    policy = {
        # expiration is iso8601 format
        'expiration': datetime.datetime.utcfromtimestamp(expire_time).isoformat() + 'Z',
        'conditions': [['starts-with', '$key', path]]
    }

    b64policy = base64.b64encode(json.dumps(policy).strip().encode())

    h = hmac.new(access_key_secret.encode(), b64policy, sha)
    signature = base64.encodebytes(h.digest()).strip()

    return {
        'access_id': access_key_id,
        'host': host,
        'policy': b64policy.decode(),
        'signature': signature.decode(),
        'expire': expire_time,
        'path': path,
        'b64callback': base64.b64encode(json.dumps(callback_obj).strip().encode()).decode()
    }


async def get_sign_url(obj, timeout):
    return bucket.sign_url('GET', obj, timeout)


