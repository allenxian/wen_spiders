from utils.base import base_spider


class kr_spider(base_spider):
    website = '36kr'

    def __init__(self):
        self.count = 67000

    def parse_news_flashes(self, begin_id):
        begin_id = begin_id
        