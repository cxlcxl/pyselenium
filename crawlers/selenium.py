import os
import time
import selenium.common.exceptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib.parse
import requests
import random
import re
from seleniumwire import webdriver


def path_filter(p):
    if p[0] == '/':
        return p[1:]
    else:
        return p


def create_a_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8, 9][random.randint(0, 4)]

    # 第三位数字
    third = {3: random.randint(0, 9),
             4: [5, 7, 9][random.randint(0, 2)],
             5: [i for i in range(10) if i != 4][random.randint(0, 8)],
             7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
             8: random.randint(0, 9), }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)

    # 拼接手机号
    return "1{}{}{}".format(second, third, suffix)


def html_ext_fill(u):
    return os.path.join(u, 'index.tmpl')


class PyCrawler:
    def __init__(self, url, chromedriver=''):
        if chromedriver == '':
            print('请指定 Google 驱动地址')
            exit()
        self.file_save_base_path = './storage/games/'
        self.url = url
        self.user_agent = 'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) ' \
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        self.blink_features = 'disable-blink-features=AutomationControlled'
        # google 浏览器调用引擎
        self.chromedriver = chromedriver

    # 创建抓取参数
    def build_options(self):
        options = Options()
        # 无头模式，不打开浏览器
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument(self.user_agent)
        # 就是这一行告诉chrome去掉了webdriver痕迹
        options.add_argument(self.blink_features)
        return options

    def save_file(self, f_url, page_source=None, ext=None):
        if page_source is None:
            return

        rs = urllib.parse.urlparse(f_url)
        f_real = os.path.join(self.file_save_base_path, rs.netloc, path_filter(rs.path))
        path_info = os.path.split(f_real)
        if not os.path.exists(path_info[0]):
            try:
                os.makedirs(path_info[0])
            except:
                print('文件路径创建失败：', path_info[0])
                return

        # fix 没有文件后缀情况
        if path_info[1] == '' and ext is not None:
            f_real = ext(f_real)

        print('保存文件为：', f_real)
        with open(f_real, 'a', encoding='utf-8') as f:
            f.write(page_source)

        return

    # 抓取只需要 url 就可以访问的游戏
    def scrapy_url_games(self, url_prefix):
        # 打开网页取到源码
        response = requests.get(self.url)
        page_source = response.text
        game_name_filter = re.compile(r"name:'(.*?)',", re.M)
        all_names = game_name_filter.findall(page_source)
        game_urls = []
        if len(all_names) > 0:
            for name in all_names:
                game_url = urllib.parse.urljoin(url_prefix, name.replace(' ', ''))
                game_urls.append(game_url)
        print(game_urls)

    # includes 额外要下载相关资源的外站
    # wait_func 页面等待方式
    # wait_time 等待时长
    def find_urls(self, includes=None, wait_func=None, download_all=False):
        if includes is None:
            includes = []

        driver = webdriver.Chrome(options=self.build_options(), seleniumwire_options={})

        host = urllib.parse.urlparse(self.url)
        includes.append(host.hostname)

        # Go to the Google home page
        driver.get(self.url)

        # driver.set_page_load_timeout(30)
        # driver.implicitly_wait(120)
        wait_func(driver)

        rs_urls = []
        # Access requests via the `requests` attribute
        for request in driver.requests:
            if request.response:
                u = urllib.parse.urlparse(request.url)
                if download_all or u.hostname in includes:
                    rs_urls.append(request.url)

        driver.close()
        return rs_urls
