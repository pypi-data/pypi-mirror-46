#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: login.py
# @time: 2019/3/15 13:01
# @Software: PyCharm


__author__ = 'A.Star'

import datetime
import requests
from snowland_authsdk.token_helper import verify_token, generate_token
from snowland_authsdk.common import (
    OAUTH_ACCESS_TOKEN_URL,
    OAUTH_AUTHORIZE_URL,
    OAUTH_USERINFO_URL,
    SNOWLAND_PUBLIC_KEY,
    PAYLOAD_DEMO
)


class Account(object):
    def __init__(self, access_key, access_secret):
        self.access_key = access_key
        self.access_secret = access_secret


class OAuth(Account):
    def oauth_authorize(self, application=None, username=None, password=None):
        """
        :param req:
        :param access_key:
        :param access_secret:
        :return:
        """
        assert application
        if username and password:
            data = {
                "username": username,
                "password": password,
                "application": application
            }
            res = requests.post(OAUTH_AUTHORIZE_URL, data=data)
        else:
            params = {
                "application": application
            }
            res = requests.get(OAUTH_AUTHORIZE_URL, params=params)
        return res.content

    def oauth_access_token(self, code, k=32, len_param=64, method='get', expire_seconds=300):
        """

        :param code:
        :param k:
        :param len_param:
        :param method: GET or POST
        :param expire_seconds: 过期时间（以秒计算的时间差）
        :return:
        """
        flag = verify_token(code, SNOWLAND_PUBLIC_KEY, len_param=len_param)
        if flag:
            payload = PAYLOAD_DEMO.copy()
            payload['iss'] = self.access_key,
            payload['sub'] = "get token"
            payload['aud'] = "snowland"
            now = datetime.datetime.now()
            payload['exp'] = (now + datetime.timedelta(seconds=expire_seconds)).strftime(
                "%Y-%m-%d %X")
            payload['iat'] = now.strftime("%Y-%m-%d %X")
            payload['nbf'] = now.strftime("%Y-%m-%d %X")
            # TODO 设置JWT ID
            payload['data'] = {"code": code}
            if method.lower() == 'get':
                this_token = generate_token(payload, self.access_secret, k, len_param, expire_seconds=expire_seconds)
                params = {
                    "token": this_token,
                    "access_key": self.access_key
                }
                req = requests.get(OAUTH_ACCESS_TOKEN_URL, params=params)
            else:
                data = {
                    'access_key': self.access_key,
                    'access_secret': self.access_secret,
                    "code": code
                }
                req = requests.post(OAUTH_ACCESS_TOKEN_URL, data=data)
            return req.content
        else:
            return None

    def oauth_userinfo(self, token):
        """
        返回用户信息
        :param req:
        :param access_key:
        :param access_secret:
        :return:
        """
        params = {
            "token": token,
            'access_key': self.access_key,
            'access_secret': self.access_secret
        }
        req = requests.get(OAUTH_USERINFO_URL, params=params)
        return req.content

