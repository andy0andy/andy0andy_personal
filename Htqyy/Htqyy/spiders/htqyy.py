# -*- coding: utf-8 -*-
import scrapy
from Htqyy.items import HtqyyItem


class HtqyySpider(scrapy.Spider):
    name = 'htqyy'
    allowed_domains = ['www.htqyy.com']
    # start_urls = ['http://www.htqyy.com/']


    def start_requests(self):
        url_list = {
            "hot":"http://www.htqyy.com/top/musicList/hot?pageIndex={}&pageSize=20",
            "new":"http://www.htqyy.com/top/musicList/new?pageIndex={}&pageSize=20",
            "recommend":"http://www.htqyy.com/top/musicList/recommend?pageIndex={}&pageSize=20",
            "_1":"http://www.htqyy.com/genre/musicList/1?pageIndex={}&pageSize=20&order=hot",
            "_3":"http://www.htqyy.com/genre/musicList/3?pageIndex={}&pageSize=20&order=hot",
            "_5":"http://www.htqyy.com/genre/musicList/5?pageIndex={}&pageSize=20&order=hot",
        }

        for key,value in url_list.items():
            for url in self.page_requests(value,key):
                # print(url)
                yield scrapy.Request(url)

    def page_requests(self,url_str,type):
        pages = {
            "hot": 25,
            "new": 5,
            "recommend": 8,
            "_1": 19,
            "_3": 16,
            "_5": 8,
        }

        for index in range(pages[type]):
            yield url_str.format(index)


    def parse(self, response):

        mItem = response.xpath("//ul/li[@class='mItem']")

        for sinfo in mItem:
            item = HtqyyItem()

            item = {
                "sid":"http://f2.htqyy.com/play7/" + sinfo.xpath(".//input/@value").get() + "/mp3/3",
                "sname":sinfo.xpath(".//span[@class='title']/a/text()").get()
            }

            yield item


