#!/usr/bin/env python
"""
 Created by howie.hu at 2019-09-12.
"""

import hashlib

import requests

from w2b.utils import logger


def gen_md5(string):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(string.encode(encoding="utf-8"))
    return hl.hexdigest()


def send_get_request(url, timeout=10, **kwargs) -> dict:
    """
    发起GET请求
    """
    try:
        resp = requests.get(url, timeout=timeout, **kwargs)
    except Exception as e:
        resp = None
        logger.exception(f"请求出错 - {url}")
    return resp
