#!/usr/bin/python
# coding:utf-8

from .. import messenger
from asyncio import get_event_loop


async def send_with_uid(uid, msg, *args):
    args = uid, msg, *args
    return await get_event_loop().run_in_executor(None, messenger.send_with_uid, *args)


async def send_directly(indicator, msg):
    args = indicator, msg
    return await get_event_loop().run_in_executor(None, messenger.send_directly, *args)
