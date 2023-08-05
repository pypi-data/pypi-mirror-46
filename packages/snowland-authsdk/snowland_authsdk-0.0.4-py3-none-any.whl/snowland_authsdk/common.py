#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: common.py
# @time: 2019/3/16 14:49
# @Software: PyCharm


__author__ = 'A.Star'

from easydict import EasyDict

hex_string = '0123456789abcdef'
hex_string_upper = '0123456789ABCDFEF'
alnum_string = '1234567890qwertyuiopasdfghjklzxcvbnm'

# base_url_auth = 'http://account.snowland.ltd'
# base_url_token = 'http://account.snowland.ltd'
base_url_auth = 'http://127.0.0.1:10005'
base_url_token = 'http://127.0.0.1:10005'
OAUTH_AUTHORIZE_URL = base_url_auth + "/o/oauth2/v2/auth"
OAUTH_ACCESS_TOKEN_URL = base_url_token + "/oauth2/v4/token"
OAUTH_USERINFO_URL = base_url_token + "/oauth2/v1/userinfo"

PAYLOAD_DEMO = EasyDict({
    "iss": None,  # Issue 发行者
    "sub": None,  # 主题
    "aud": None,  # Audience，观众
    "exp": None,  # Expiration time，过期时间
    "nbf": None,  # Not before
    "iat": None,  # Issued at，发行时间
    "jti": None,  # JWT ID
})

SNOWLAND_PUBLIC_KEY = 'b1d24c20b223c8e57c3da05ce831964eef9081969cffa9972d5a072e633f2860e2cf8920fdf84e960402254c0fd2d9706e973315580fa39b3eb5c4d4ea5548be'
