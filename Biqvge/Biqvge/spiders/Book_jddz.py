# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Biqvge.items import BiqvgeItem

class BookJddzSpider(CrawlSpider):
    name = 'Book_jddz'
    allowed_domains = ['www.biquge001.com']
    start_urls = ['http://www.biquge001.com/Book/0/194/']

    rules = (
        Rule(LinkExtractor(allow=r'.*Book/0/194/\d+?.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        item = BiqvgeItem()

        item['bookname'] = response.xpath("//div[@class='bookname']/h1/text()").get()
        item['content'] = response.xpath("string(//div[@id='content'])").get().replace("\xa0","").replace("</p>","")

        # print(item)
        yield item