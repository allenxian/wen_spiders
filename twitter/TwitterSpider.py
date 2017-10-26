from utils.base import BaseSpider
from utils.config import MONGO_CLIENT

from TwitterAPI import TwitterAPI
import time
import json
from parsel import Selector

class TwitterSpider(BaseSpider):
    # api part
    consumer_key = '0S6siec5MhdPlReKc5y1EgFbE'
    consumer_secret = 'sq0AE7Xtalvx001TyPl6NwzFptuCntHprveyO69drh8yDtAZXb'
    access_token = '862235971361710080-wnK3bwTONdXZ7UoX9mJBWTVAqE4Ub1k'
    access_token_secret = 'wbsFax1dxtqO5zduBMPJWc9PRNFACNQvifNT84pgBOUpc'

    # tweepy
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)

    # TwitterAPI
    api = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

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

    ## function
    def get_tweets(self):
        coll = MONGO_CLIENT['twitter']['tweet_status']
        with open('twitter/rts2016-clusters.txt') as f:
            lines = f.readlines()
            for line in lines:
                time.sleep(0.5)
                parts = line.split('\t')
                tweet_id = parts[2].replace('\n', '')
                one_tweet = {}
                one_tweet['_id'] = tweet_id
                one_tweet['content'] = self.get_status(tweet_id)
                self.save_doc(coll, one_tweet)

    def get_status(self, tweet_id):
        repo = self.api.request('statuses/show/:%s' % tweet_id)
        return repo.text

    def load_docs(self):
        good_count = 0
        coll = MONGO_CLIENT['twitter']['tweet_status']
        for doc in coll.find():
            content_dict = json.loads(doc['content'])
            if 'text' in content_dict:
                good_count += 1
                # print(content_dict['text'], content_dict['created_at'])
        print(good_count)

    ## test
    def get_test(self):
        repo = self.api.request('statuses/show/:%s' % self.demo_tweet_id)
        return repo

    def add_cluster_id(self):
        # add cluster id
        coll_1 = MONGO_CLIENT['twitter']['tweet_status']
        coll_2 = MONGO_CLIENT['twitter']['tweet_status_new']
        id_dict = {}
        with open('twitter/rts2016-clusters.txt') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.split('\t')
                tweet_id = parts[2].replace('\n', '')
                cluster_id = parts[1]
                id_dict[tweet_id] = cluster_id
        for doc in coll_1.find():
            new_doc = doc
            new_doc['cluster_id'] = id_dict[doc['_id']]
            self.save_doc(coll_2, new_doc)






if __name__ == '__main__':
    spider  = TwitterSpider()
    # spider.get_tweets()
    spider.add_cluster_id()