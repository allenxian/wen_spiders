import requests
from utils.user_agents import random_ua
from kr.config import MONGO_CLIENT, DB_NAME


class BaseSpider(object):
    website = 'base'
    key_name = 'base'

    def __init__(self):
        self.key = self.generate_key()
        self.coll = self.db['%s_%s' % (self.website, self.key_name)]
        self.HEADERS = {'User-Agent': random_ua()}

    def parse_value(self, response, selector, all=True):
        if all:
            rlts = filter(lambda value: value.strip() != '',
                          response.xpath(selector).extract())
            return map(lambda rlt: rlt.strip(), rlts)
        else:
            rlt = response.xpath(selector).extract_first()
            if rlt:
                return rlt.strip()
            return ''

    @property
    def db(self):
        return MONGO_CLIENT[DB_NAME]

    @property
    def random_header(self):
        self.HEADERS.update({'User-Agent': random_ua()})
        return self.HEADERS

    def p_get(self, url):
        headers = self.random_header
        return requests.get(url, headers=headers)

    def generate_key(self):
        return '{website}_{key_name}'.format(website=self.website, key_name=self.key_name)

    def save_doc(self, coll, doc):
        try:
            coll.insert_one(doc)
        except Exception as e:
            print(e)
