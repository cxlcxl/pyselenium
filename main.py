from crawlers.selenium import PyCrawler
from crawlers.game_fm import game_fm_wait_func, GameFmCrawl
from crawlers.utils import md5


if __name__ == '__main__':
    game_num = '1'
    surl = f'https://static.game.fm/data/{game_num}/index.html'
    crawler = PyCrawler(surl, chromedriver='./runtime/chromedriver.exe')
    urls = crawler.find_urls(wait_func=game_fm_wait_func)

    game_key = md5(game_num)[:12]
    game_fm = GameFmCrawl(save_base=f'gamesources/{game_key}/', game_numeric=game_num)
    game_fm.fetch_source(urls)
