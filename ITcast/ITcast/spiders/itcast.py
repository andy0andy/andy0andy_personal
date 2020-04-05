# -*- coding: utf-8 -*-
import scrapy

from ITcast.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['www.itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):

        li_txt = response.xpath("//div[@class='li_txt']")

        for node in li_txt:
            # 创建item字段，用来存储数据
            item = ItcastItem()

            item["name"] = node.xpath("./h3/text()").get()
            item["title"] = node.xpath("./h4/text()").get()
            item["info"] = node.xpath("./p/text()").get()

            # 将数据返回给 pipelines管道
            yield item
