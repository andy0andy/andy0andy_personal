# -*- coding: utf-8 -*-
import scrapy
from QSDBK.items import QsdbkItem

class QiushidabaikeSpider(scrapy.Spider):
    name = 'qiushidabaike'
    allowed_domains = ['qiushidabaike.com']
    start_urls = ['http://qiushidabaike.com/text_1.html/']

    def parse(self, response):
        main_list = response.xpath("//dl[@class='main-list']")

        for node in main_list:
            item = QsdbkItem()

            item['title'] = node.xpath("./dt/span/a/text()").get()

            if node.xpath("./dd[@class='content']/p/text()"):
                item['content'] = node.xpath("./dd[@class='content']/p/text()").get().strip()
            else:
                item['content'] = node.xpath("./dd[@class='content']/text()").get().strip()

            item['fr'] = node.xpath("./dt/p/span[@class='fr']/text()").get().strip()

            yield item

        next_page = response.xpath("//a[@class='next']/@href").get()

        if next_page:
            next_url = 'http://qiushidabaike.com' + next_page

            yield scrapy.Request(next_url,callback=self.parse)
