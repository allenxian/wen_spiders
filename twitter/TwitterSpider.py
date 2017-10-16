from utils.base import BaseSpider
import time
from parsel import Selector

class TwitterSpider(BaseSpider):
    # api
    tweet_api = 'https://twitter.com/statuses/%s'

    ## demo
    demo_tweet_id = '762005409519448065'

    ## test
    def get_test(self):
        repo = self.p_get(self.tweet_api % self.demo_tweet_id)
        return repo.text


if __name__ == '__main__':
    spider  = TwitterSpider()
    print(spider.get_test())
