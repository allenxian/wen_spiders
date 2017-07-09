# -*- coding: utf-8 -*-
from utils.base import BaseSpider
import time
from parsel import Selector


class WordsSpider(BaseSpider):
    # xpath
    sublist_x = '//div[@id="entries-selector"]//ul//li//a/@href'
    page_x = '//ul[@class="paging_links inner"]//a/@href'
    words_x = '//div[@id="entrylist1"]//li//text()'
    # url
    base_url = 'http://www.oxfordlearnersdictionaries.com/us/wordlist/english/academic/'
    # the urls of sublist
    sublist_url = []
    # the url of page of each sublist
    page_url = []

    def parse_words(self, url):
        resp0 = self.p_get(url)
        hxs = Selector(text=resp0.text)
        word_list = self.parse_value(hxs, self.words_x)
        return list(word_list)

    def parse(self):
        self.sublist_url.append(self.base_url)

        # build the sublist_url
        print('building the sublist_url...')
        resp = self.p_get(self.base_url)
        hxs = Selector(text=resp.text)
        self.sublist_url += self.parse_value(hxs, self.sublist_x)

        # build the page_url
        print('building the page_url...')
        for url in self.sublist_url:
            time.sleep(1)
            resp0 = self.p_get(url)
            hxs = Selector(text=resp0.text)
            inner_list = self.parse_value(hxs, self.page_x)
            for inner in inner_list:
                if inner not in self.page_url:
                    self.page_url.append(inner)

        # parse the word and write to file
        print('parsing the words and writing to file...')
        with open('oxford_words.txt', 'w') as words_f:
            # get the words of sublist_url
            for url in self.page_url:
                word_list = self.parse_words(url)
                print(url)
                print(str(len(word_list)) + 'words')
                for word in word_list:
                    words_f.write(word + '\n')

            # get the words of page_url
            for url in self.sublist_url:
                word_list = self.parse_words(url)
                print(url)
                print(str(len(word_list)) + 'words')
                for word in word_list:
                    words_f.write(word + '\n')


if __name__ == '__main__':
    words_spider = WordsSpider()
    words_spider.parse()
