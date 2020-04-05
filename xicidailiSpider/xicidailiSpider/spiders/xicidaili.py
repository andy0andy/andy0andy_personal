# -*- coding: utf-8 -*-
import scrapy


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn']

    def parse(self, response):
        trs = response.xpath("//tr")

        for tr in trs:
            ip = tr.xpath("./td[2]/text()").get()     # 获取IP
            port = tr.xpath("./td[3]/text()").get()       # 获取端口
            addr = tr.xpath("./td[4]/a/text()").get()       # 地址
            type = tr.xpath("./td[6]/text()").get()     # 类型

            item = {
                'IP':ip,
                'PORT':port,
                "ADDR":addr,
                "TYPE":type,
            }
            yield item

        # 翻页操作
        next_page= response.xpath("//a[@class='next_page']//@href").get()
        # print(next_page)
        if next_page:

            # 拼接url 并返回一个 请求 给parse方法处理
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url,callback=self.parse)