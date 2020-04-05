# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItcastItem(scrapy.Item):
    # define the fields for your item here like:

    # 黑马老师名字
    name = scrapy.Field()
    # 黑马老师职位
    title = scrapy.Field()
    # 黑马老师简介
    info = scrapy.Field()




    # pass
