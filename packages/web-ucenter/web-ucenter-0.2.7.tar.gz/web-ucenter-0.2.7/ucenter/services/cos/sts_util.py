#!/usr/bin/env python
# coding=utf-8

from .sts import Sts
from tweb import snowflake
import config

cfg = {
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 1800,
        # 固定密钥
        'secret_id': 'AKIDKRN8h2LjjT0LRNpeuvgCTVJrGm35cSnv',
        # 固定密钥
        'secret_key': '50g7LL6ctvjNmvqW5U1MXTBdy83tXzFG',
        'proxy': {
        },
        # 换成你的 bucket
        'bucket': 'photos-1256296813',
        # 换成 bucket 所在地区
        'region': 'ap-guangzhou',
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的目录，例子：* 或者 a/* 或者 a.jpg
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/14048
        'allow_actions': [
            # 简单上传
            'name/cos:PutObject',
            # 分片上传
            'name/cos:InitiateMultipartUpload',
            'name/cos:ListMultipartUploads',
            'name/cos:ListParts',
            'name/cos:UploadPart',
            'name/cos:CompleteMultipartUpload'
        ]
    }


def get_sts(user_id):
    instance_id = config.Port * 100 + config.ID
    file_id = snowflake.Snowflake(instance_id).generate()
    path = '{}/{}/{}'.format('private', user_id, file_id)

    cfg['allow_prefix'] = path + '.*'
    sts = Sts(cfg)
    response = sts.get_credential()
    response['path'] = path
    return response
