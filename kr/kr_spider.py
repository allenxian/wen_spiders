from utils.base import base_spider
from kr.config import REDIS_CLIENT

class kr_spider(base_spider):
    website = 'kr'

    # news flashes template
    news_flashes_tpl = 'http://kr.com/api/info-flow/newsflash_columns/newsflashes?b_id=%s&per_page=%s'

    def __init__(self):
        self.count = 50000

    def parse_news_flashes(self, cur_id):
        per_page = 20
        cur_url = self.news_flash_tpl % (cur_id, per_page)
        resp = self.p_get(cur_url)

    def make_ids(self):
        for num in range(2500):
            id = 15000 + num * 20

