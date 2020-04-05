# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery as pq

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    start_urls = ['https://login.taobao.com/member/login.jhtml']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):

        print(response.xpath("//a[@class='J_ClickStat']/text()").getall())
