# coding:utf-8

from tweb.error_exception import ErrException, ERROR
import uuid
from ucenter.services import user_indicate
from ucenter.db import mongo as db
from tweb.json_util import filter_keys
import time
from bson.objectid import ObjectId


def list_all():
    cursor = db.users.find({})
    array = list()
    for item in cursor:
        item['id'] = item['_id'].__str__()
        item.pop('_id')

        out_filter(item)
        array.append(item)
    return array


def add(data):
    user_id = data.get('id')
    if user_id is None:
        raise ErrException(ERROR.E40005, extra='not set id when adding user')

    data['_id'] = ObjectId(user_id)
    data.pop('id')

    now = int(time.time() * 1000)
    data['created'] = now
    data['updated'] = now
    db.users.insert_one(data)
    return get(user_id)


def get(indicator, unsafely=False):
    """
    根据用户名，手机号，邮箱或者用户ID获取用户信息
    :param indicator: 用户名，手机号，邮箱或者用户ID
    :param unsafely: 不完全模式读取，为True时即把密码等敏感信息也完全读出
    :return: user对象
    """
    indicator = indicator.lower()
    try:
        uuid.UUID(indicator)
        key = 'id'
    except ValueError:
        if user_indicate.is_user_id(indicator):
            key = '_id'
            indicator = ObjectId(indicator)
        elif user_indicate.is_email(indicator):
            key = 'email'
        elif user_indicate.is_mobile(indicator):
            key = 'mobile'
        elif user_indicate.is_username(indicator):
            key = 'name'
        else:
            raise ErrException(ERROR.E40002)

    user = db.users.find_one({key: indicator})
    if user is None:
        return None

    user['id'] = user['_id'].__str__()
    user.pop('_id')

    if not unsafely:
        return out_filter(user)
    else:
        return user


def get_with_open_id(platform, open_id, unsafely=False):
    """
    根据第三方平台open_id获取用户信息
    :param platform: 平台名，如weixin, weibo等
    :param open_id: 第三方平台分配的用户唯一标示
    :param unsafely: 不完全模式读取，为True时即把密码等敏感信息也完全读出
    :return: user对象
    """

    key = '{}.open_id'.format(platform)
    user = db.users.find_one({key: open_id})
    if user is None:
        return None

    user['id'] = user['_id'].__str__()
    user.pop('_id')

    if not unsafely:
        return out_filter(user)
    else:
        return user


def get_with_union_id(platform, union_id, unsafely=False):
    """
    根据第三方平台open_id获取用户信息
    :param platform: 平台名，如weixin, wxmp(小程序), weibo等
    :param union_id: 第三方平台分配的统一用户唯一标示（如微信在APP，公众号，小程序间用UnionID标示同一个用户）
    :param unsafely: 不完全模式读取，为True时即把密码等敏感信息也完全读出
    :return: user对象
    """

    key = '{}.union_id'.format(platform)
    user = db.users.find_one({key: union_id})
    if user is None:
        return None

    user['id'] = user['_id'].__str__()
    user.pop('_id')

    if not unsafely:
        return out_filter(user)
    else:
        return user


def out_filter(user):
    """
    输出给用户是，出于安全考虑，以及格式要求，进行过滤操作
    :param user: 用户对象
    :return: user 过滤后的用户对象
    """
    if user is None:
        return user

    if user.get('pwd_hash') is None:
        user['has_pwd'] = 0
    else:
        user['has_pwd'] = 1

        user.pop('pwd_hash')
        user.pop('salt')

    # user.pop('status')

    # for key in list(user):
    #     if user[key] is None:
    #         user.pop(key)

    return user


def update(user_id, data):
    """
    修改用户资料
    :param user_id: 用户 id
    :param data: 新数据
    :return:
    """
    new_data = filter_keys(data, {
        'nickname': 1,
        'gender': 1,
        'country': 1,
        'province': 1,
        'city': 1,
        'icon': 1,
        'birthday': 1
    })

    now = int(time.time() * 1000)
    new_data['updated'] = now

    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': new_data})
    return get(user_id)


def update_oauth(platform, oauth):
    """
    更新第三方平台用户信息
    :param platform: 平台名
    :param oauth: 新数据
    :return:
    """
    open_id = oauth.get('open_id')
    new_data = filter_keys(oauth, {
        'open_id': 1,
        'union_id': 1,
        'nickname': 1,
        'icon': 1,
        'extend': 1
    })

    key = '{}.open_id'.format(platform)
    db.users.update_one({key: open_id}, {'$set': {platform: new_data}})
    return get_with_open_id(platform, open_id)


def bind(user_id, key, indicator):
    """
    绑定手机或邮箱
    :param user_id: 用户 id
    :param key: 绑定的类型
    :param indicator: 手机号码或邮箱
    :return: user 对象
    """
    if key == 'email' and not user_indicate.is_email(indicator):
        raise ErrException(ERROR.E40003)

    if key == 'mobile' and not user_indicate.is_mobile(indicator):
        raise ErrException(ERROR.E40004)

    new_data = {key: indicator}

    now = int(time.time() * 1000)
    new_data['updated'] = now

    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': new_data})

    return get(user_id)


def update_bind(user_id, key, indicator):
    """
    换绑手机
    :param user_id: 用户 id
    :param key: 绑定的类型
    :param indicator: 新手机号码
    :return: user 对象
    """
    if key == 'email':
        # 邮箱不支持换绑
        raise ErrException(ERROR.E40000)

    ret = bind(user_id, key, indicator)
    return ret


def bind_oauth(user_id, platform, oauth):
    """
    绑定第三方平台用户
    :param user_id: 用户ID
    :param platform: 平台名
    :param oauth: 开放平台用户信息
    :return: user对象
    """
    new_data = {
        platform: filter_keys(oauth, {
            'open_id': 1,
            'union_id': 1,
            'nickname': 1,
            'icon': 1,
            'extend': 1
        })
    }

    now = int(time.time() * 1000)
    new_data['updated'] = now

    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': new_data})

    return get(user_id)


def unbind_oauth(user_id, platform):
    """
    解除绑定的第三方平台用户
    :param user_id: 用户ID
    :param platform: 平台名
    :return: user对象
    """

    now = int(time.time() * 1000)
    db.users.update_one({'_id': ObjectId(user_id)}, {'$unset': {platform: 1}, '$set': {'updated': now}})

    return get(user_id)


def set_name(user_id, name):
    """
    设置用户名
    :param user_id: 用户 id
    :param name: 用户名
    :return: user 对象
    """
    new_data = {'name': name}

    now = int(time.time() * 1000)
    new_data['updated'] = now

    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': new_data})

    return get(user_id)


def set_pwd(data):
    """
    设置密码
    :param data: 包含 用户 id：user_id; 新密码：pwd_hash; 盐值: salt
    :return: user对象
    """
    user_id = data.get('user_id')

    new_data = filter_keys(data, {'pwd_hash': 1, 'salt': 1})

    now = int(time.time() * 1000)
    new_data['updated'] = now

    db.users.update_one({'_id': ObjectId(user_id)}, {'$set': new_data})

    return get(user_id)
