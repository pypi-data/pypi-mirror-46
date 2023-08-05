#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: decorator.py
# @time: 2019/5/6 13:53
# @Software: PyCharm


__author__ = 'A.Star'

from functools import wraps
from snowland_authsdk.common import PAYLOAD_DEMO
import datetime
from decorator import decorator


def token_timeout(payload, fmt='%Y-%m-%d %X', expire_seconds=None):
    """
    :param payload:
    :param fmt: 时间字符串格式
    :param expire_seconds: 过期秒数，若这个参数不为None,
     则与payload['exp']所提供的过期时间比较, 比较结果应为两者熟早
    :return:
    """
    assert payload['exp'] is not None
    now = datetime.datetime.now()
    exp = datetime.datetime.strptime(payload['exp'], fmt)
    if now > exp:
        return False
    iat = datetime.datetime.strptime(payload['iat'], fmt)
    if iat is not None and expire_seconds is not None:
        exp = iat + datetime.timedelta(seconds=expire_seconds)
        if now > exp:
            return False
    return True


@decorator
def logging(func, *args, **kwargs):
    print("[DEBUG] {}: enter {}()".format(datetime.datetime.now(), func.__name__))
    return func(*args, **kwargs)


if __name__ == '__main__':
    pass

