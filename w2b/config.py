#!/usr/bin/env python
"""
 Created by howie.hu at 2019-09-12.
"""

import os

from w2b.utils.tools import gen_md5


class Config:
    # 微信发送账户ID
    S_ACCOUNT_ID = os.environ.get("S_ACCOUNT_ID", "")
    # 微信接收账户ID
    R_ACCOUNT_ID = os.environ.get("R_ACCOUNT_ID", "")
    # 解密Key
    RAW_KEY = os.environ.get("RAW_KEY", "")
    # 消息DB路径
    DB_PATH_TEM = "/Users/howie6879/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/{0}/Message/"
    # 微信接收账户所有消息DB文件夹
    MSG_DB_DIR = DB_PATH_TEM.format(gen_md5(R_ACCOUNT_ID))
    # 与目标微信账户的聊天表
    MSG_TABLE_NAME = f"Chat_{gen_md5(S_ACCOUNT_ID)}"
    # 笔记Tag
    BEAR_TAG = "资源/微信"
    # 多久扫描一次，单位是S
    INTERVAL = 10
