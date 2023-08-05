#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: sign.py
# @time: 2019/5/6 9:48
# @Software: PyCharm


__author__ = 'A.Star'

from abc import ABCMeta, abstractmethod
from pysmx.SM2 import Sign as sm2_sign
from pysmx.SM2 import Verify as sm2_verify


class Sign(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def signature(encoded_string, secret, rand=None, len_param=64, *args, **kwargs):
        pass


class SM2Sign(Sign):
    @staticmethod
    def signature(encoded_string, secret, rand, len_param=64, encoding='utf-8', *args, **kwargs):
        assert isinstance(rand, str)
        assert isinstance(encoding, str)
        return sm2_sign(encoded_string, secret, rand, len_para=len_param, encoding=encoding)


class Verify(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def verify(encoded_string, secret, rand=None, len_param=64, *args, **kwargs):
        pass


class SM2Verify(Verify):
    @staticmethod
    def verify(sign, message, public, len_param=64, *args, **kwargs):
        return sm2_verify(sign, message, public, len_para=len_param)
