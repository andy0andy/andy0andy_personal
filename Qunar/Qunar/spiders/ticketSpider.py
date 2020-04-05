# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from Qunar.items import QunarItem


class TicketspiderSpider(CrawlSpider):
    name = 'ticketSpider'
    allowed_domains = ['qunar.com']
    start_urls = ['https://piao.qunar.com/ticket/list.htm?keyword=广州&region=&from=mps_search_suggest']

    rules = (
        Rule(LinkExtractor(allow=r'.*ticket/list.+?page=\d+?'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sight_item = response.xpath("//div[@class='sight_item']")

        for sight in sight_item:

            item = QunarItem()

            item['title'] = sight.xpath(".//a[@class='name']/text()").get()
            level = sight.xpath(".//span[@class='level']/text()")
            if level:
                item['level'] = level.get()
            else:
                item['level'] = '---'
            item['addr'] = sight.xpath(".//p[@class='address color999']/span/text()").get().lstrip("地址：")
            item['tip'] = sight.xpath(".//div[@class='intro color999']/text()").get()
            item['price'] = sight.xpath("string(.//span[@class='sight_item_price'])").get().replace(r"\xa","")

            yield item