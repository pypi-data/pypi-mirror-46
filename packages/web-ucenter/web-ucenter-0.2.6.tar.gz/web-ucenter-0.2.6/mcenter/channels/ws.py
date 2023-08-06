from tornado.websocket import WebSocketError
import asyncio

ws_sessions = dict()


def send_msg(uid, msg):
    """
    发送websocket消息
    :param uid: 用户ID
    :param msg: {
        'title': '标题',
        'greetings': '问候',
        'content': '内容',
        'sender': '发送者落款',
        'ps': '附加信息，如公司官网地址'
    }
    """

    wsh = ws_sessions.get(uid)
    if wsh is not None:
        try:
            # 需要加上这句，否则报错："There is no current event loop in thread ..."
            asyncio.set_event_loop(asyncio.new_event_loop())
            # END

            wsh.write_message(msg)
        except WebSocketError:
            del ws_sessions[uid]


def add_user_channel(uid, websocket_handler):
    ws_sessions[uid] = websocket_handler


def remove_user_channel(uid):
    del ws_sessions[uid]
