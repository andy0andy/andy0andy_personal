# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from LiePin.items import LiepinItem


class LiepinSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=python']

    rules = (
        # 分页
        Rule(LinkExtractor(allow=r'.*/zhaopin/.+?&curPage=\d+?'), follow=True),
        # 进一步爬取
        Rule(LinkExtractor(allow=r'.*https://www.liepin.com.+?\.shtml'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = LiepinItem()

        # print("1->", type(item))

        item['title'] = response.xpath("//div[@class='about-position']//h1/text()").get(),
        item['comp']=response.xpath("//div[@class='about-position']//h3/a/text()").get(),
        item['money']=response.xpath("//div[@class='about-position']//p[@class='job-item-title']/text()").get().replace("\r\n","").replace(" ",""),
        item['addr']=response.xpath("//div[@class='about-position']//p[@class='basic-infor']/span/a/text()").get(),
        item['fuli']=response.xpath("string(//div[@class='about-position']//ul[@class='comp-tag-list clearfix'])").get().replace("\r\n","").replace(" ",""),
        item['job_yaoqiu']=response.xpath("string(//div[@class='about-position']//div[@class='job-qualifications'])").get().replace("\r\n","").replace(" ",""),
        item['job_content']=response.xpath("string(//div[@class='about-position']//div[@class='content content-word'])").get(),

        # print("2->",type(item))
        return item
