#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: token.py
# @time: 2019/3/19 10:40
# @Software: PyCharm

import datetime
import json
from pysmx.SM2 import generate_keypair
from base64 import urlsafe_b64encode, urlsafe_b64decode
# from pysmx.SM2 import Sign, Verify
from snowland_authsdk.util import random_hex_string
from snowland_authsdk.decorator import token_timeout
from snowland_authsdk.sign import Sign, SM2Sign, SM2Verify, Verify
__author__ = 'A.Star'


def generate_token(payload: dict, secret=None, k=32, len_param=64, encoding='utf-8', alg='SM2',rand=None, **kwargs):
    """
    生成token, JWT 标准,
    参考： https://ninghao.net/blog/2834
    :param payload: dict 验证token时需要返回的信息
    :param secret: 私钥
    :param k: 16进制随机数的长度
    :param len_param: SM2签名参数，目前只支持64
    :return: token
    """
    assert len_param == 64
    if isinstance(alg, type) and issubclass(alg, Sign):
        header = b'{"alg":"%s"}' % bytes(alg.name, encoding)
        SignAlgorithm = alg
    else:
        if isinstance(alg, str):
            header = b'{"alg":"%s"}' % bytes(alg, encoding)
        elif isinstance(alg, (bytes, bytearray)):
            header = b'{"alg":"%s"}' % alg
            alg = str(alg, encoding=encoding)
        assert alg in ['SM2', 'RSA']
        if alg == 'SM2':
            SignAlgorithm = SM2Sign
        elif alg == 'RSA':
            raise NotImplementedError
        else:
            return None
    rand = payload.get('rand', None) or rand
    if rand is None:
        rand = random_hex_string(k)
    if isinstance(rand, (bytes, bytearray)):
        rand = str(rand, encoding=encoding)
    payload['rand'] = rand
    payload = bytes(json.dumps(payload), encoding=encoding)
    encoded_string = urlsafe_b64encode(header) + b"." + urlsafe_b64encode(payload)
    signed = SignAlgorithm.signature(str(encoded_string, encoding=encoding), secret, rand, len_para=len_param)
    b = encoded_string + b'.' + urlsafe_b64encode(bytes(signed, encoding=encoding))
    return str(b, encoding=encoding)


def verify_token(token: (bytes, str), publickey, len_param=64, expire_seconds=3600, * ,encoding='utf-8', **kwargs):
    """
    验证token有效性
    :param token: generate_token生成的token
    :param publickey: 公钥
    :param len_param: 密钥长度
    :return: 如果token无效，返回None,否则返回payload
    """
    if isinstance(token, str):
        token = bytes(token, encoding=encoding)
    split_token = token.split(b'.')
    assert len(split_token) == 3
    header = json.loads(urlsafe_b64decode(split_token[0]))
    payload = json.loads(urlsafe_b64decode(split_token[1]))
    e = split_token[0] + b'.' + split_token[1]
    # TODO：其他算法header
    alg = header['alg'].upper()
    assert alg in ['SM2', 'RSA']
    if alg == 'SM2':
        VerifyAlgorithm = SM2Verify
    else:
        return None
    signed = str(urlsafe_b64decode(split_token[2]), encoding=encoding)
    # 签名检验
    # print("verify::", signed)
    # print("v-rand:", payload['rand'])
    if not VerifyAlgorithm.verify(signed, e, publickey, len_param):
        return None
    if not token_timeout(payload, expire_seconds=expire_seconds):
        return None
    return payload


if __name__ == '__main__':
    pk, sk = generate_keypair()
    pay = {"CODE": 123}
    # token = generate_token(pay, sk)
    # v = verify_token(token, pk)
    sign = Sign("ABCDEF", sk, "123", 64)
    v = Verify(sign, "ABCDEF", pk, 64)
    print("v:", v)
