#!/usr/bin/env python
"""
 Created by howie.hu at 2019-09-12.
"""

import hashlib

import html2text
import requests

from lxml import etree
from w2b.utils import logger


def gen_md5(string):
    # 创建md5对象
    hl = hashlib.md5()
    hl.update(string.encode(encoding="utf-8"))
    return hl.hexdigest()


def send_get_request(url, timeout=10, **kwargs):
    """
    发起GET请求
    """
    try:
        resp = requests.get(url, timeout=timeout, **kwargs)
    except Exception as e:
        resp = None
        logger.exception(f"请求出错 - {url}")
    return resp


def wechat2md(element: etree._Element):
    main_article = etree.tostring(element, encoding="utf-8").decode(encoding="utf-8")
    h = html2text.HTML2Text()
    h.ul_item_mark = "-"
    # h.body_width = 0
    main_md = h.handle(main_article)
    return main_md


if __name__ == "__main__":
    url = "https://mp.weixin.qq.com/s/qRQO9xMvGTQL-ysolXJAxQ"
    resp = send_get_request(url=url)
    doc = etree.HTML(resp.text)
    main_element = doc.cssselect("#js_content")[0]
    main_md = wechat2md(main_element)
    print(main_md)
