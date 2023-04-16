import os.path
import time
import re
import urllib.parse

import requests

from crawlers.utils import download_source

GAME_FM_WAIT_TIMEOUT = 35
game_numerics = (
    # 1, 52, 14, 60, 7, 14, 83, 67, 15, 64, 4, 98, 87, 81, 97, 10, 57, 28, 82, 85, 45, 80, 99, 31, 79, 84, 86, 22, 88,
    # 101, 106, 102, 112, 115, 1259, 123, 129, 149, 151, 153, 156, 191, 195, 217, 227, 158, 163, 161, 179, 188, 200,
    # 172, 175, 259, 264, 265, 270, 271, 272, 273, 295, 299, 296, 297, 298, 308, 278, 333, 334, 335, 240, 238, 348, 351,
    332, 354, 356,
    320, 377, 378, 379, 282, 288, 294, 331, 381, 256, 329, 391, 398, 303, 402, 367, 330, 372, 307, 409, 410, 411, 397,
    321, 389, 420, 390, 423, 430, 413, 380, 443, 446, 447, 370, 394, 437, 292, 357, 461, 369, 462, 371, 445, 464, 465,
    431, 466, 342, 467, 468, 469, 474, 475, 386, 442, 418, 451, 426, 454, 488, 417, 490, 491, 440, 495, 505, 476, 416,
    428, 405, 463, 518, 522, 448, 523, 434, 449, 450, 480, 453, 427, 525, 441, 531, 521, 506, 533, 473, 537, 484, 538,
    470, 487, 407, 520, 500, 502, 492, 419, 526, 436, 496, 400, 528, 501, 456, 554, 511, 512, 507, 510, 513, 412, 444,
    566, 527, 485, 570, 373, 572, 573, 574, 576, 577, 432, 404, 582, 586, 588, 534, 547, 550, 619, 620, 626, 627, 628,
    532, 535, 542, 631, 652, 653, 622, 654, 655, 569, 632, 656, 666, 555, 667, 668, 559, 670, 557, 624, 551, 623, 585,
    556, 629, 630, 625, 515, 517, 258, 514, 499, 516, 529, 433, 932, 933, 935, 936, 937, 938, 934, 1144, 1145, 1146,
    1147, 1148, 1149, 1156, 1158, 1170, 1171, 1172, 1173, 1180, 1182, 1092, 1164, 1193, 1194, 1196, 1152, 1155, 1174,
    1198, 1151, 1199, 1200, 1203, 1204, 1205, 1169, 1206, 1192, 1207, 1090, 1208, 1209, 1175, 1179, 1150, 1091, 1181,
    1154, 1212, 1214, 1202, 1166, 1094, 1211, 1227, 1177, 1153, 1176, 1239, 1242, 1244, 1165, 1245, 1178, 1216, 1217,
    1229, 1254, 1201, 1257, 1232, 1234, 1238, 1219, 1248, 1189, 1226, 1225, 1188, 1167, 1190, 1195, 1213, 1163, 1210,
    1222, 1243, 1168, 1255, 1253, 1218, 1223, 1221, 1231, 1237, 1256, 1240, 1224, 1197, 1258, 1191, 1228, 1215, 1246,
    1230, 1220, 1236, 1247, 1233, 1235, 1261, 1260, 1262, 1093
)


def game_fm_wait_func(driver):
    # 显示等待  无效，页面还在加载中也返回了 'complete'，canvas 画布隐式等待没有发现合适 dom 可设置
    # WebDriverWait(driver, 180).until(lambda x: x.execute_script('return document.readyState') == 'complete')
    time.sleep(GAME_FM_WAIT_TIMEOUT)


class GameFmCrawl:
    wait_timeout = 10
    save_base = ''
    game_numeric = 1
    game_info = {}

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

        return self.game_info

    def fetch_file(self, u):
        url_parse = urllib.parse.urlparse(u)
        save_path = os.path.join(self.save_base, url_parse.path.replace(f'/data/{self.game_numeric}/', ''))

        res = requests.get(u)
        if save_path.endswith('index.html'):
            # self.fill_game_info(res.text)
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

    # 提取游戏名称
    def fill_game_info(self, txt):
        fs = re.compile(r"<title>(?P<game_name>.*?)</title>", re.M)
        info = fs.finditer(txt)
        for item in info:
            self.game_info['name'] = item.group('game_name')
