from utils.base import base_spider


class kr_spider(base_spider):
    website = '36kr'

    # news flashes template
    news_flashes_tpl = 'http://36kr.com/api/info-flow/newsflash_columns/newsflashes?b_id=%s&per_page=%s'

    def __init__(self):
        self.count = 5000

    def parse_news_flashes(self, cur_id):
        per_page = 20
        cur_url = self.news_flash_tpl % (cur_id, per_page)
        resp = self.p_get(cur_url)
        

