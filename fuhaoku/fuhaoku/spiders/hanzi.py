# -*- coding: utf-8 -*-
import scrapy
from fuhaoku.items import FuhaokuItem


class HanziSpider(scrapy.Spider):
    name = 'hanzi'
    allowed_domains = ['www.fuhaoku.net']
    start_urls = ['https://www.fuhaoku.net/zi/']

    def parse(self, response):

        item = FuhaokuItem()
        trs = response.xpath("//tbody/tr")

        # 获取第一个 ？开头汉字大全
        head = trs.xpath("./th/p/text()").get()
        # ？开头的所有 拼英汉字
        zi = []


        # 行 循环
        # 如果不是标题，则加入 列表 zi
        # 如果是标题，判断是否 head 一致，不一致则表示已记录到一个字母开头的所有字并添加进 item
        for tr in  trs:
            if tr.xpath("./th"):
                if head != tr.xpath("./th/p/text()").get():
                    item['title'] = head
                    head = tr.xpath("./th/p/text()").get()

                    item['content'] = zi
                    zi = []

                    # print(item['title'], item['content'], sep="\n")
                    yield item
            else:
                for i in tr.xpath("./td/p/text()").getall():
                    zi.append(i.strip().replace(r'\r\n',''))

        item['title'] = head
        item['content'] = zi
        # print(item['title'], item['content'], sep="\n")
        yield item