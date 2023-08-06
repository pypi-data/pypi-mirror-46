import config
from tornado.websocket import WebSocketError
import asyncio
from tweb import access_token
from tweb import rdpool
import os
import json
import logging


msg_channel = '{}/mc/message'.format(config.PLATFORM)
stop_cmd_channel = None

ws_sessions = dict()
ws_pub_sessions = dict()
ws_pri_sessions = dict()


def start():
    if stop_cmd_channel is None:
        asyncio.get_event_loop().run_in_executor(None, _start)


def stop():
    if stop_cmd_channel is not None:
        rdpool.rds.publish(stop_cmd_channel, '')


def _start():
    global stop_cmd_channel

    logging.info('websocket messenger started')
    p = rdpool.rds.pubsub()

    stop_cmd_channel = '{}/stop/{}'.format(msg_channel, os.urandom(12).hex())
    p.subscribe([msg_channel, stop_cmd_channel])

    for item in p.listen():
        if item['type'] != 'message':
            continue
        channel = item['channel']
        if channel == stop_cmd_channel:
            break

        data = item['data']
        try:
            data = json.loads(data)
        except json.decoder.JSONDecodeError:
            continue
        uid = data.get('uid')
        msg = data.get('msg')
        if msg is None:
            continue

        _send_msg(msg, uid)

    logging.info('websocket messenger stopped')


def send_msg(msg, uid=None):
    data = {
        'uid': uid,
        'msg': msg
    }
    ret = rdpool.rds.publish(msg_channel, json.dumps(data))
    return ret


def _send_msg(msg, uid=None):
    """
    发送websocket消息
    :param msg: {
        'title': '标题',
        'greetings': '问候',
        'content': '内容',
        'sender': '发送者落款',
        'ps': '附加信息，如公司官网地址'
    }
    :param uid: 用户ID, 有效：发送私信，None：发送公共消息
    """

    if uid is None:
        array = ws_pub_sessions
        for wsh in array:
            _send(wsh, msg)
    else:
        array = ws_pri_sessions.get(uid)
        if array is not None:
            for token in array:
                wsh, auth = array[token]
                uid = auth['uid']
                token = auth['access_token']
                remote_ip = auth['remote_ip']
                valid = access_token.verify(uid, token, remote_ip)
                if valid:
                    _send(wsh, msg)


def _send(ws_handler, msg):
    try:
        # 需要加上这句，否则报错："There is no current event loop in thread ..."
        asyncio.set_event_loop(asyncio.new_event_loop())
        # END

        ws_handler.write_message(msg)
    except WebSocketError:
        pass


def add_channel(ws_handler, **kwargs):
    if len(kwargs) == 3:
        uid = kwargs.get('uid')
        token = kwargs.get('access_token')
        remote_ip = kwargs.get('remote_ip')
        auth = {
            'uid': uid,
            'access_token': token,
            'remote_ip': remote_ip
        }

        user_group = ws_pri_sessions.get(uid)
        if user_group is not None:
            existed = user_group.get(token)
            if existed is not None:
                wsh = existed[0]
                wsh.close()
                del ws_pub_sessions[wsh]
                del user_group[token]
        else:
            ws_pri_sessions[uid] = dict()

        ws_pub_sessions[ws_handler] = auth
        ws_pri_sessions[uid][token] = (ws_handler, auth)
    else:
        ws_pub_sessions[ws_handler] = None


def remove_channel(ws_handler):
    if ws_handler not in ws_pub_sessions:
        return

    auth = ws_pub_sessions.get(ws_handler)
    if auth is not None:
        uid = auth['uid']
        token = auth['access_token']
        if uid in ws_pri_sessions and token in ws_pri_sessions[uid]:
            del ws_pri_sessions[uid][token]

    del ws_pub_sessions[ws_handler]
