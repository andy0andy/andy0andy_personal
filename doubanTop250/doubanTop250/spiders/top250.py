# -*- coding: utf-8 -*-
import scrapy
from doubanTop250.items import Doubantop250Item


class Top250Spider(scrapy.Spider):
    name = 'top250'
    # allowed_domains = ['movie.douban.com/top250']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        lis = response.xpath("//ol[@class='grid_view']/li").extract()

        for li in lis:
            item = Doubantop250Item()

            item['img'] = li.xpath("./div/div/a/img/@src").get()
            item['title'] = li.xpath(".//a/span[position()=1]/text()").get()
            item['rating_num'] = li.xpath(".//span[@class='rating_num']/text()").get()
            item['author'] = li.xpath(".//div[@class='bd']/p/text()").get().strip(" \n")
            item['inq'] = li.xpath(".//span[@class='inq']/text()").get()

            # print(item)
            yield item

        # 翻页
        next_page = response.xpath("//span[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page,callback=self.parse)