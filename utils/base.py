import requests
from utils.user_agents import random_ua


class base_spider(object):
    def __init__(self):
        self.xsrf = ''

    def parse_value(self, response, selector, all=False):
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
    def random_header(self):
        self.HEADERS.update({'User-Agent': random_ua()})
        return self.HEADERS

    def p_get(self, url):
        headers = self.random_header
        return requests.get(url, headers=headers)
