import scrapy


class GamefmSpider(scrapy.Spider):
    name = "gamefm"
    allowed_domains = ["game.fm"]
    prefix = "https://static.game.fm/data/"
    save_base_path = "./gamefm/"
    start_urls = ["https://static.game.fm/data/1/index.html"]

    def parse(self, response):
        pass
