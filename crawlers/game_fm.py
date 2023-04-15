import os.path
import time
import re
import urllib.parse

import requests

from crawlers.utils import download_source

GAME_FM_WAIT_TIMEOUT = 10


def game_fm_wait_func(driver):
    # 显示等待  无效，页面还在加载中也返回了 'complete'，canvas 画布隐式等待没有发现合适 dom 可设置
    # WebDriverWait(driver, 180).until(lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(GAME_FM_WAIT_TIMEOUT)


class GameFmCrawl:
    wait_timeout = 10
    save_base = ''
    game_numeric = 1

    def __init__(self, save_base, game_numeric=1):
        self.save_base = save_base
        self.game_numeric = game_numeric

    def fetch_source(self, urls):
        for _url in urls:
            rs = self.fetch_file(_url)
            if rs is False:
                print('Fail 文件下载失败：', _url)
            else:
                print('Success:', _url)

    def fetch_file(self, u):
        url_parse = urllib.parse.urlparse(u)
        save_path = os.path.join(self.save_base, url_parse.path.replace(f'/data/{self.game_numeric}/', ''))

        res = requests.get(u)
        if save_path.endswith('index.html'):
            self.find_url_in_html(u, res.text)

        return download_source(res.content, save_path)

    def find_url_in_html(self, u, txt):
        fs = re.compile(r"href=\"(.*?)\"", re.M)
        local_files = fs.findall(txt)
        urls = []
        if len(local_files) > 0:
            for f in local_files:
                if f.startswith('http'):
                    continue
                furl = urllib.parse.urljoin(u, f)
                urls.append(furl)

        if len(urls) > 0:
            self.fetch_source(urls)
