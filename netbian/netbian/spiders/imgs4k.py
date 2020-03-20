# -*- coding: utf-8 -*-
import scrapy
from netbian.items import NetbianItem


class Imgs4kSpider(scrapy.Spider):
    name = 'imgs4k'
    allowed_domains = ['pic.netbian.com']
    start_urls = [
            'http://pic.netbian.com/4kfengjing',
            'http://pic.netbian.com/4kmeinv',
            'http://pic.netbian.com/4kyouxi',
            'http://pic.netbian.com/4kdongman',
            'http://pic.netbian.com/4kyingshi',
            'http://pic.netbian.com/4kmingxing',
            'http://pic.netbian.com/4kqiche',
            'http://pic.netbian.com/4kdongwu',
            'http://pic.netbian.com/4krenwu',
            'http://pic.netbian.com/4kmeishi',
            'http://pic.netbian.com/4kzongjiao',
            'http://pic.netbian.com/4kbeijing',

    ]

    def parse(self, response):
        item = NetbianItem()

        item['imgurl'] = response.xpath("//ul[@class='clearfix']/li/a/img/@src").getall()
        item['imgname'] = response.xpath("//ul[@class='clearfix']/li/a/img/@alt").getall()
        item['dirname'] = response.xpath("//div[@class='classify clearfix']/a[@class='curr']/text()").get()

        yield item

        next_page = response.xpath("//div[@class='page']/a[last()-1]/@href").get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)