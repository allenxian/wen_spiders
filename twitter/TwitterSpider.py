from utils.base import BaseSpider
import tweepy
import requests
import time
from parsel import Selector

class TwitterSpider(BaseSpider):
    # api part
    consumer_key = '0S6siec5MhdPlReKc5y1EgFbE'
    consumer_secret = '	sq0AE7Xtalvx001TyPl6NwzFptuCntHprveyO69drh8yDtAZXb'
    access_token = '862235971361710080-wnK3bwTONdXZ7UoX9mJBWTVAqE4Ub1k'
    access_token_secret = 'wbsFax1dxtqO5zduBMPJWc9PRNFACNQvifNT84pgBOUpc'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


    # proxy
    proxies = {
        'https': 'https://127.0.0.1:1080',
        'http': 'http://127.0.0.1:1080'
    }

    # opener = requests.build_opener(requests.ProxyHandler(proxies))
    # requests.install_opener(opener)

    # api
    tweet_api = 'https://twitter.com/statuses/%s'

    ## demo
    demo_tweet_id = '762005409519448065'

    ## test
    def get_test(self):
        repo = self.api.get_status(self.demo_tweet_id)
        return repo


if __name__ == '__main__':
    spider  = TwitterSpider()
    print(spider.get_test())
