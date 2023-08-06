import json
from tornado import httpclient
import config
from tweb import rdpool
from tweb.error_exception import ErrException, ERROR


async def get_access_token_async(code):
    """
    根据微信授权码 code 获取 access_token
    :param code:
    :return: access_token 对象
    """
    # 从 redis 中获取 access_token
    record = restore_access_token(code)

    if record is not None:
        access_token = record['access_token']
        openid = record['openid']
        expires_in = record['expires_in']
        refresh_token = record['refresh_token']

        # 判断 access_token 是否有效
        if await verify_access_token_async(access_token, openid):
            # 有效则检查 expires_in 判断是否需要刷新 access_token
            if expires_in < 300:
                # 有效时间小于 5 分钟时则刷新 access_token, 并更新 redis
                record = await refresh_access_token_async(code, refresh_token)
        else:
            # 刷新 access_token, 并更新 redis
            record = await refresh_access_token_async(code, refresh_token)

            # ---------------------------------------------
            # code 只能使用一次，无法再次获取
            # 无效则删除 redis 重新获取
            # remove_access_token(code)
            # 删除缓存重新在微信服务器获取 access_token 对象
            # record = await get_access_token_async(code)
            # ---------------------------------------------
        return record

    # 从微信服务器获取 access_token
    # 微信 app id
    app_id = config.WeiXin['appid']
    # 微信 secret
    secret = config.WeiXin['secret']
    grant_type = 'authorization_code'

    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
          'appid={}&secret={}&code={}&grant_type={}'\
        .format(app_id, secret, code, grant_type)

    http_client = httpclient.AsyncHTTPClient()
    try:
        response = http_client.fetch(url)
        data = json.loads(response.body.decode('utf-8'))

        if 'errcode' in data:
            raise ErrException(ERROR.E50003, extra='error from wechat: ' + json.dumps(data))

        store_access_token(code, data, data.get('expires_in'))
        return data

    except httpclient.HTTPError as e:
        raise ErrException(ERROR.E50003, extra='request error: [%s] %s' % (e.args[0], e.args[1]), e=e)
    except ErrException as e:
        raise e
    except Exception as e:
        raise ErrException(ERROR.E50003, extra=e.args[0], e=e)


async def refresh_access_token_async(code, refresh_token):
    """
    刷新 access_token
    :param code: 微信授权码
    :param refresh_token:
    :return: access_token 对象
    """
    app_id = config.WeiXin['appid']
    url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?' \
          'appid={}&grant_type=refresh_token&refresh_token={}'.format(app_id, refresh_token)
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
        data = json.loads(response.body.decode('utf-8'))

        if 'errcode' in data:
            raise ErrException(ERROR.E50003, extra='error from wechat: ' + json.dumps(data))

        store_access_token(code, data, data.get('expires_in'))
        return data
    except httpclient.HTTPError as e:
        raise ErrException(ERROR.E50003, extra='request error: [%s] %s' % (e.args[0], e.args[1]), e=e)
    except ErrException as e:
        raise e
    except Exception as e:
        raise ErrException(ERROR.E50003, extra=e.args[0], e=e)


async def verify_access_token_async(access_token, openid):
    """
    验证 access_token 是否有效
    :param access_token:
    :param openid:
    :return: bool
    """
    url = 'https://api.weixin.qq.com/sns/auth?' \
          'access_token={}&openid={}'.format(access_token, openid)
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
        data = json.loads(response.body.decode('utf-8'))

        return data.get('errcode') == 0
    except httpclient.HTTPError as e:
        raise ErrException(ERROR.E50003, extra='request error: [%s] %s' % (e.args[0], e.args[1]), e=e)
    except ErrException as e:
        raise e
    except Exception as e:
        raise ErrException(ERROR.E50003, extra=e.args[0], e=e)


async def get_user_info_async(access_token, openid):
    """
    获取用户信息
    :param access_token:
    :param openid:
    :return: user_info
    """
    url = 'https://api.weixin.qq.com/sns/userinfo?' \
          'access_token={}&openid={}'.format(access_token, openid)
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch(url)
        data = json.loads(response.body.decode('utf-8'))

        if 'errcode' in data:
            raise ErrException(ERROR.E50003, extra='error from wechat: ' + json.dumps(data))

        return data
    except httpclient.HTTPError as e:
        raise ErrException(ERROR.E50003, extra='request error: [%s] %s' % (e.args[0], e.args[1]), e=e)
    except ErrException as e:
        raise e
    except Exception as e:
        raise ErrException(ERROR.E50003, extra=e.args[0], e=e)


def restore_access_token(code):
    key = _key(code)
    data = rdpool.rds.get(key)

    if data is None:
        return None

    record = json.loads(data)
    # 更新过期时间
    record['expires_in'] = rdpool.rds.ttl(key)
    return record


def store_access_token(code, data, timeout):
    rdpool.rds.set(_key(code), json.dumps(data), timeout)


def remove_access_token(code):
    rdpool.rds.delete(_key(code))


def _key(code):
    return '{}/user/weixin/{}'.format(config.PLATFORM, code)
