#!/usr/bin/env python
"""
 Created by howie.hu at 2019-09-12.
"""
import os
import time
import sys

import schedule

from urllib.parse import quote_plus
from lxml import etree

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from w2b.config import Config
from w2b.sqlite_db import get_target_db_path, init_db
from w2b.utils import logger
from w2b.utils.tools import send_get_request

latest_query_time = int(time.time())


def monitor_msg(cur):
    global latest_query_time
    cur_time = int(time.time())
    query_sql = f"""select * from {Config.MSG_TABLE_NAME} where msgCreateTime>={latest_query_time} and msgCreateTime<{cur_time} order by msgCreateTime desc"""
    # logger.info(query_sql)
    res = cur.execute(query_sql)
    for i in res.fetchall():
        msg_type = i[6]
        # 分享类型文章
        if msg_type == 49:
            msg_content = i[3]
            doc = etree.fromstring(msg_content)
            doc_type = doc.cssselect("type")[0].text
            # 公众号文章
            if int(doc_type) == 5:
                doc_url = doc.cssselect("url")[0].text
                parse_url(doc_url)
    latest_query_time = cur_time


def parse_url(url):
    resp = send_get_request(url=url)
    if resp:
        doc = etree.HTML(resp.text)

        title = doc.cssselect("meta[property='og:title']")[0].get("content")
        description = doc.cssselect("meta[property='og:description']")[0].get("content")
        image = doc.cssselect("meta[property='og:image']")[0].get("content")

        main_article = etree.tostring(
            doc.cssselect("#js_content")[0], encoding="utf-8"
        ).decode(encoding="utf-8")

        bear_cmd = f"bear://x-callback-url/create?title={quote_plus(title)}&text={quote_plus(resp.url)}&tags={quote_plus(Config.BEAR_TAG)}&open_note=no"
        logger.info(f"文章 {title} 同步成功")
        cmd = f"open '{bear_cmd }'"
        os.system(cmd)

    else:
        logger.error(f"抓取：{url} 失败")


def run():
    db_path = get_target_db_path()
    _, cur = init_db(db_path=db_path)

    schedule.every(Config.INTERVAL).seconds.do(monitor_msg, cur)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run()
