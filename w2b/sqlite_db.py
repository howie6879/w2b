#!/usr/bin/env python
"""
 Created by howie.hu at 2019-09-12.
"""

import os

from pysqlcipher3 import dbapi2 as sqlite

from w2b.config import Config
from w2b.utils import logger


def init_db(db_path):
    """连接数据库"""
    conn = sqlite.connect(db_path)
    cur = conn.cursor()
    cur.execute(f'''PRAGMA key= "x'{Config.RAW_KEY}'"''')
    cur.execute("PRAGMA cipher_page_size=1024")
    cur.execute("PRAGMA kdf_iter = 64000")
    cur.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA1")
    cur.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1")
    return conn, cur


def get_target_db_path():
    """获取目标数据库"""
    msg_db_dir = Config.MSG_DB_DIR
    msg_table_name = Config.MSG_TABLE_NAME
    for file in os.listdir(msg_db_dir):
        if str(file).endswith(".db"):
            db_path = msg_db_dir + file
            conn, cur = init_db(db_path=db_path)
            # 查询表 f"Chat_{target_table_name}" 是否存在
            is_exist = cur.execute(
                f"""SELECT count(*) FROM sqlite_master WHERE type="table" AND name = "{msg_table_name}" """
            ).fetchall()[0][0]
            if is_exist:
                logger.info(f"目标表 {msg_table_name} 存在于库 {file}")
                return db_path
    return ""


if __name__ == "__main__":
    # db_path = "/Users/howie6879/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/988eebd1023a0d794bff2b6f5c8d5176/Contact/wccontact_new2.db"
    # conn, cur = init_db(db_path)
    # cur.execute("select * from WCContact limit 5;")

    print(get_target_db_path())
