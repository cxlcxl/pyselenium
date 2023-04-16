import time

from crawlers.selenium import PyCrawler
from crawlers.game_fm import game_fm_wait_func, GameFmCrawl, game_numerics
from crawlers.utils import md5

if __name__ == '__main__':
    for item in game_numerics:
        game_num = str(item)
        game_id = md5(game_num)[:12]
        save_dir = f'gamesources/{game_num}-{game_id}/'

        surl = f'https://static.game.fm/data/{game_num}/index.html'
        crawler = PyCrawler(surl, chromedriver='./runtime/chromedriver.exe')
        urls = crawler.find_urls(wait_func=game_fm_wait_func)

        game_fm = GameFmCrawl(save_base=save_dir, game_numeric=game_num)
        game_info = game_fm.fetch_source(urls)
        print("----------------- 游戏抓取完成 -----------------")

        time.sleep(5)
