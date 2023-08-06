# coding=utf-8

import config

from ..http_handler.user.send_code import SendCodeGenerating
from ..http_handler.user.code_verify import CodeVerify
from ..http_handler.user.identify import UserIdentifying
from ..http_handler.user.logout import LogoutHandling
from ..http_handler.user.register import RegisterHandling
from ..http_handler.user.login.with_code import CodeLogging
from ..http_handler.user.login.with_pwd import PwdLogging
from ..http_handler.user.login.with_weixin import WeixinLogging
from ..http_handler.user.login.with_wxmp import WxmpLogging
from ..http_handler.user.update.bind_with_weixin import WeixinBinding
from ..http_handler.user.update.bind_with_code import CodeBinding
from ..http_handler.user.update.update_common import CommonUpdating
from ..http_handler.user.update.unbind_weixin import WeixinUnBinding
from ..http_handler.user.update.set_name import NameSetting
from ..http_handler.user.update.set_password import PasswordSetting, PasswordResetting
from ..http_handler.user.user_info import UserInfoGetting

base = '{}/{}/uc'.format(config.VER, config.PLATFORM)
routes = [
    # 请求验证码(sms)
    (r"/%s/code/sms" % base, SendCodeGenerating),

    # 请求验证码(email)
    (r"/%s/code/email" % base, SendCodeGenerating),

    # 校验验证码
    (r"/%s/code/verify" % base, CodeVerify),

    # 获取用户ID
    (r"/%s/identify" % base, UserIdentifying),

    # 用户名注册
    (r"/%s/register" % base, RegisterHandling),

    # 密码登陆
    (r"/%s/login/pwd" % base, PwdLogging),

    #  验证码登陆
    (r"/%s/login/code" % base, CodeLogging),

    #  微信认证登录
    (r"/%s/login/weixin" % base, WeixinLogging),

    # 微信小程序登录
    (r"/%s/login/wxmp" % base, WxmpLogging),

    #  登出
    (r"/%s/logout" % base, LogoutHandling),

    #  设置用户名
    (r"/%s/set/name" % base, NameSetting),

    #  设置密码/修改密码
    (r"/%s/set/password" % base, PasswordSetting),

    # 重置密码
    (r"/%s/reset/password" % base, PasswordResetting),

    #  根据code绑定绑定手机号或者邮箱（与获取code的方式有关）
    (r"/%s/bind/code" % base, CodeBinding),

    #  绑定微信
    (r"/%s/bind/weixin" % base, WeixinBinding),

    #  解绑微信
    (r"/%s/unbind/weixin" % base, WeixinUnBinding),

    #  修改用户资料
    (r"/%s/update" % base, CommonUpdating),

    # 读取用户信息
    (r'/%s/user_info' % base, UserInfoGetting)
]
