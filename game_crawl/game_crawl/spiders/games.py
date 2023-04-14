from pathlib import Path
import urllib.parse
import scrapy


class GamesSpider(scrapy.Spider):
    name = "games"
    prefix = "https://static.game.fm/data/1/"

    def start_requests(self):
        urls = [
            {"_url": 'https://static.game.fm/data/1/index.html', "base": 'https://static.game.fm/data/1/'},
        ]

        for url in urls:
            self.build_game_info(url)
            yield scrapy.Request(url=url["_url"], callback=self.parse)

    def build_game_info(self, url):
        print(url)
        # yield scrapy.Request(url=url["_url"], callback=self.parse)

    def parse(self, response, **kwargs):
        # page = response.url.split("/")[-2]
        # filename = f'quotes-{page}.html'
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')
        # 解析页面获取代码
        u = urllib.parse.urlparse(response.url)
        print(response.url, u, response.text)

        game_info = {
            "name": "",
            "game_id": "",
            "save_path": "",
            "state": "",
        }

        # 传输到 pipelines
        yield game_info

        # try:
        #     # /html/head/script[7]
        #     page = response.xpath("//div[@class='page']/a[last()]/@href").get()
        #     next_url = self.prefix + page
        #     if not page:
        #         print("爬取完毕，退出爬虫")
        #         return
        #     else:
        #         print("下一页地址：{}".format(next_url))
        #         yield scrapy.Request(next_url)
        # except Exception as e:
        #     print("异常", e)
        #     return

