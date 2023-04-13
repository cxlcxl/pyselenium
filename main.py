from crawlers.selenium import PyCrawler
from crawlers.game_fm import game_fm_wait_func, fetch_source


if __name__ == '__main__':
    surl = 'https://static.game.fm/data/1/index.html'
    crawler = PyCrawler(surl, chromedriver='./runtime/chromedriver')
    urls = crawler.find_urls(wait_func=game_fm_wait_func)
    fetch_source(urls, 'game-fm/1/')
