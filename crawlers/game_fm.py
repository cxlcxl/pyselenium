import os.path
import time
import asyncio
import urllib.parse

import aiohttp
import aiofiles


GAME_FM_WAIT_TIMEOUT = 10


def game_fm_wait_func(driver):
    # 显示等待  无效，页面还在加载中也返回了 'complete'，canvas 画布隐式等待没有发现合适 dom 可设置
    # WebDriverWait(driver, 180).until(lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(GAME_FM_WAIT_TIMEOUT)


def fetch_source(urls, save_base):
    tasks = []
    for _url in urls:
        t = format_static(_url, save_base)
        tasks.append(t)

    print(tasks)


def format_static(u, save_base):
    url_parse = urllib.parse.urlparse(u)
    save_path = os.path.join(save_base, url_parse.path.replace('/data/1/', ''))
    return {"url": u, "save_path": save_path}
