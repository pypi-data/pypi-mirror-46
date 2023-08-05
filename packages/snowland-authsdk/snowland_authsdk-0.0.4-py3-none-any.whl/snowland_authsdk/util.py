#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: util.py
# @time: 2019/3/19 10:47
# @Software: PyCharm


__author__ = 'A.Star'

from random import choices
from snowland_authsdk.common import (
    hex_string_upper, hex_string, alnum_string
)


def random_string(n: int=32):
    return ''.join(choices(alnum_string, k=n))


def random_hex_string(n: int=32, upper=False):
    return ''.join(choices(hex_string_upper, k=n)) if upper else ''.join(choices(hex_string, k=n))
