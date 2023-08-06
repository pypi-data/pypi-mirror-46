#!/usr/bin/python
# coding:utf-8

from ucenter.services import ctrl_user
from asyncio import get_event_loop


async def list_all():
    return await get_event_loop().run_in_executor(None, ctrl_user.list_all)


async def add(data):
    args = (data,)
    return await get_event_loop().run_in_executor(None, ctrl_user.add, *args)


async def get(indicator, unsafely=False):
    args = indicator, unsafely
    return await get_event_loop().run_in_executor(None, ctrl_user.get, *args)


async def get_with_open_id(platform, open_id, unsafely=False):
    args = platform, open_id, unsafely
    return await get_event_loop().run_in_executor(None, ctrl_user.get_with_open_id, *args)


async def get_with_union_id(platform, union_id, unsafely=False):
    args = platform, union_id, unsafely
    return await get_event_loop().run_in_executor(None, ctrl_user.get_with_union_id, *args)


async def update(user_id, data):
    args = user_id, data
    return await get_event_loop().run_in_executor(None, ctrl_user.update, *args)


async def update_oauth(platform, oauth):
    args = platform, oauth
    return await get_event_loop().run_in_executor(None, ctrl_user.update_oauth, *args)


async def bind(user_id, key, indicator):
    args = user_id, key, indicator
    return await get_event_loop().run_in_executor(None, ctrl_user.bind, *args)


async def update_bind(user_id, key, indicator):
    args = user_id, key, indicator
    return await get_event_loop().run_in_executor(None, ctrl_user.update_bind, *args)


async def bind_oauth(user_id, platform, oauth_info):
    args = user_id, platform, oauth_info
    return await get_event_loop().run_in_executor(None, ctrl_user.bind_oauth, *args)


async def unbind_oauth(user_id, platform):
    args = user_id, platform
    return await get_event_loop().run_in_executor(None, ctrl_user.unbind_oauth, *args)


async def set_name(user_id, name):
    args = user_id, name
    return await get_event_loop().run_in_executor(None, ctrl_user.set_name, *args)


async def set_pwd(data):
    args = (data,)
    return await get_event_loop().run_in_executor(None, ctrl_user.set_pwd, *args)
