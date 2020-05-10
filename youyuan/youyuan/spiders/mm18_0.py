# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_redis.spiders import RedisCrawlSpider

from youyuan.items import YouyuanItem


class Mm180Spider(RedisCrawlSpider):
    name = 'mm18-0'
    # allowed_domains = ['http://www.youyuan.com/find/shenzhen/mm18-0/advance-0-0-0-0-0-0-0/p1/']
    # start_urls = ['http://www.youyuan.com/find/shenzhen/mm18-0/advance-0-0-0-0-0-0-0/p1/']

    redis_key = "mm18_0:start_urls"

    rules = (
        Rule(LinkExtractor(allow=r'.*/find/shenzhen/mm18-0/advance-0-0-0-0-0-0-0/p\d+?/'), follow=True),        # 分页
        Rule(LinkExtractor(allow=r'.*/\d+?-profile/'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()

        item = YouyuanItem()

        item["name"] = response.xpath("//div[@class='main']/strong/text()").get().strip()
        local = response.xpath("//p[@class='local']/text()").get().split(" ")
        l = [i for i in local if len(i) > 0]
        item["now_in"] = l[0].strip()
        item["age"] = l[1].strip()
        item["hoby"] = [i.strip().replace(r"\xa0","") for i in response.xpath("//ol[@class='hoby']/li/text()").getall()]
        item["pics"] = response.xpath("//ul[@class='block_photo']/li/a/img/@src").getall()
        item["monologue"] = response.xpath("//ul[@class='requre']/li/p/text()").get().strip()
        item["native_place"] = response.xpath("//div[@class='message']/ol[1]/li[position()=1]/span[@class='black']/text()").getall()[0].strip()
        item["weight"] = response.xpath("//div[@class='message']/ol[1]/li[position()=2]/span[@class='black']/text()").getall()[0].strip()
        item["degree"] = response.xpath("//div[@class='message']/ol[1]/li[position()=3]/span[@class='black']/text()").getall()[0].strip()
        item["salary"] = response.xpath("//div[@class='message']/ol[1]/li[position()=4]/span[@class='black']/text()").get().strip()
        item["wang_kid"] = response.xpath("//div[@class='message']/ol[1]/li[position()=5]/span[@class='black']/text()").get().strip()
        item["like_type"] = response.xpath("//div[@class='message']/ol[1]/li[position()=6]/span[@class='black']/text()").get().strip()
        item["live_parents"] = response.xpath("//div[@class='message']/ol[1]/li[position()=7]/span[@class='black']/text()").get().strip()
        item["marriage"] = response.xpath("//div[@class='message']/ol[2]/li[position()=1]/span[@class='black']/text()").getall()[0].strip()
        item["height"] = response.xpath("//div[@class='message']/ol[2]/li[position()=2]/span[@class='black']/text()").getall()[0].strip()
        item["job"] = response.xpath("//div[@class='message']/ol[2]/li[position()=3]/span[@class='black']/text()").getall()[0].strip()
        item["house"] = response.xpath("//div[@class='message']/ol[2]/li[position()=4]/span[@class='black']/text()").getall()[0].strip()
        item["remote"] = response.xpath("//div[@class='message']/ol[2]/li[position()=5]/span[@class='black']/text()").getall()[0].strip()
        item["sex"] = response.xpath("//div[@class='message']/ol[2]/li[position()=6]/span[@class='black']/text()").getall()[0].strip()
        item["charm_part"] = response.xpath("//div[@class='message']/ol[2]/li[position()=7]/span[@class='black']/text()").getall()[0].strip()
        item["half_addr"] = response.xpath("//div[@class='message']/ol[1]/li[position()=1]/span[@class='black']/text()").getall()[1].strip()
        item["half_height"] = response.xpath("//div[@class='message']/ol[1]/li[position()=2]/span[@class='black']/text()").getall()[1].strip()
        item["half_salary"] = response.xpath("//div[@class='message']/ol[1]/li[position()=3]/span[@class='black']/text()").getall()[1].strip()
        item["half_degree"] = response.xpath("//div[@class='message']/ol[2]/li[position()=2]/span[@class='black']/text()").getall()[1].strip()
        item["half_age"] = response.xpath("//div[@class='message']/ol[2]/li[position()=1]/span[@class='black']/text()").getall()[1].replace(" ","")

        # print(item)
        return item
