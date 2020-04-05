# -*- coding: utf-8 -*-
import scrapy
from imgSpider.items import ImgspiderItem

class TianjiaimgSpider(scrapy.Spider):
    name = 'tianjiaimg'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = [
        'http://lab.scrapyd.cn/archives/55.html',
        'http://lab.scrapyd.cn/archives/57.html',
    ]

    def parse(self, response):
        imgurl = response.xpath("//p/img/@src").getall()
        imgdirname = response.xpath("//h1[@class='post-title']/a/text()").getall()
        item = ImgspiderItem()
        item['imgurl'] = imgurl
        item['imgdirname'] = imgdirname

        yield item