import os
import scrapy
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options


def make_all_dirs(p, filepath=False):
    if filepath is True:
        filepath, fullname = os.path.split(p)
        print(filepath, fullname)

    if not os.path.isdir(p):
        os.makedirs(p)


class GamesSpider(scrapy.Spider):
    name = "games"
    prefix = "https://static.game.fm/data/1/"
    file_save_base_path = './games/'
    user_agent = 'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) ' \
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    blink_features = 'disable-blink-features=AutomationControlled'
    # google 浏览器调用引擎
    chromedriver = 'chromedriver'

    def start_requests(self):
        # base 最后不能以 / 结尾
        urls = [
            {"_url": 'https://static.game.fm/data/521/index.html', "base": 'https://static.game.fm/data/521',
             "game_id": '6666'},
        ]

        for url in urls:
            yield scrapy.Request(url=url["_url"], callback=self.parse,
                                 cb_kwargs={"game_id": url["game_id"], "base": url["base"]})

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

    def parse(self, response, **kwargs):
        self.download_index_page(response.text, kwargs["game_id"])

        # driver = webdriver.Chrome(options=self.build_options(), seleniumwire_options={})

        # Go to the Google home page
        # driver.get(response.url)

        # driver.set_page_load_timeout(30)
        # driver.implicitly_wait(120)
        # 网页加载完成用 js 设置无效
        # time.sleep(15)

        # Access requests via the `requests` attribute
        # for request in driver.requests:
        #     if request.response:
        #         yield scrapy.Request(url=request.url, callback=self.download_source, cb_kwargs=kwargs)
        #
        # driver.close()

    def download_source(self, response, **kwargs):
        source_url = response.url
        bs = os.path.join(self.file_save_base_path, kwargs["game_id"])
        _file = source_url.replace(kwargs['base'], bs)

        with open(_file, mode="a", encoding='utf-8') as f:
            f.write(response.text)

        file_info = {
            "save_path": _file,
            "game_id": kwargs["game_id"],
        }
        yield file_info

    def download_index_page(self, bs, game_id):
        p = os.path.join(self.file_save_base_path, game_id)

        print(66666666666)
        _file = os.path.join(p, "index.html")
        make_all_dirs(_file, filepath=True)
        with open(_file, mode="a", encoding='utf-8') as f:
            f.write(bs)

        file_info = {
            "save_path": _file,
            "game_id": game_id,
        }
        yield file_info
