#!/usr/bin/python
# coding:utf-8

from .. import ctrl_msg_tpl
from asyncio import get_event_loop


async def add(name, data):
    args = (name, data,)
    return await get_event_loop().run_in_executor(None, ctrl_msg_tpl.add, *args)


async def get(name):
    args = (name,)
    return await get_event_loop().run_in_executor(None, ctrl_msg_tpl.get, *args)
