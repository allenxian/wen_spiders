from kr.config import REDIS_CLIENT
from utils.base import BaseSpider
import json


class FlashesSpider(BaseSpider):
    website = 'kr'
    key_name = 'flashes'
    # test url
    # news flashes template
    news_flashes_tpl = 'http://36kr.com/api/info-flow/newsflash_columns/newsflashes?b_id=%s&per_page=%s'

    def __init__(self):
        super(FlashesSpider, self).__init__()
        self.limit = 15000

    def parse_news_flashes(self, cur_id):
        per_page = 20
        cur_url = self.news_flashes_tpl % (cur_id.decode("utf-8"), per_page)
        print(cur_url)
        resp = self.p_get(cur_url).text
        resp_json = json.loads(resp)
        news_list = resp_json['data']['items']
        for news in news_list:
            news.update({'_id': news['id']})
            try:
                self.save_doc(self.coll, news)
            except Exception as e:
                print(e)


    def make_id_set(self, begin_id):
        good_id = begin_id
        while good_id > self.limit:
            good_id -= 20
            REDIS_CLIENT.sadd(self.key,
                              good_id)
        print('--------> finish making id set <--------')
        print('we have %s id now' % REDIS_CLIENT.scard(self.key))

    def multi_thread(self):
        pass

    def process(self, begin_id):
        self.make_id_set(begin_id)
        while REDIS_CLIENT.scard(self.key) > 0:
            the_id = REDIS_CLIENT.spop(self.generate_key())
            try:
                self.parse_news_flashes(the_id)
            except Exception as e:
                print(e)
                # REDIS_CLIENT.sadd(self.key, the_id)


if __name__ == '__main__':
    flash_spider = FlashesSpider()
    flash_spider.process(67672)
