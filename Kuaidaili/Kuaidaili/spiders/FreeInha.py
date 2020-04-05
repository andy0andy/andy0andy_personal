# -*- coding: utf-8 -*-
import scrapy
from Kuaidaili.items import KuaidailiItem

class FreeinhaSpider(scrapy.Spider):
    name = 'FreeInha'
    allowed_domains = ['www.kuaidaili.com']
    # start_urls = ['https://www.kuaidaili.com/free/inha/{}/']

    def start_requests(self):
        urls = 'https://www.kuaidaili.com/free/inha/{}/'

        for i in range(1,3371):
            url = urls.format(i)
            yield scrapy.Request(url)

    def parse(self, response):

        trs = response.xpath("//tbody/tr")

        for tr in trs:
            item = KuaidailiItem()

            ip = tr.xpath(".//td[position()=1]/text()").get()
            port = tr.xpath(".//td[position()=2]/text()").get()
            type = tr.xpath(".//td[position()=4]/text()").get()

            item['proxy'] = type + "://" + ip + ":" + port
            item['position'] = tr.xpath(".//td[position()=5]/text()").get()
            item['speed'] = tr.xpath(".//td[position()=6]/text()").get()

            # print(item)

            yield item


