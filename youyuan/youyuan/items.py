# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YouyuanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    now_in = scrapy.Field()     # 现居地
    age = scrapy.Field()
    hoby = scrapy.Field()
    pics = scrapy.Field()   # 照片墙
    monologue = scrapy.Field()      # 独白
    native_place = scrapy.Field()  # 籍贯
    weight = scrapy.Field()  # 体重
    degree = scrapy.Field()  # 学历
    salary = scrapy.Field()  # 月薪
    wang_kid = scrapy.Field()  # 是否想要小孩
    like_type = scrapy.Field()  # 喜欢的类型
    live_parents = scrapy.Field()  # 是否愿意与父母同住
    marriage = scrapy.Field()  # 婚姻
    height = scrapy.Field()  # 身高
    job = scrapy.Field()
    house = scrapy.Field()  # 住房
    remote = scrapy.Field()  # 能否接受异地恋
    sex = scrapy.Field()  # 能否接受婚前性行为
    charm_part = scrapy.Field()  # 最有魅力的部位
    half_addr = scrapy.Field()  # 另一半所在地区
    half_height = scrapy.Field()  # 另一半身高
    half_salary = scrapy.Field()  # 另一半收入
    half_degree = scrapy.Field()  # 另一半学历
    half_age = scrapy.Field()  # 另一半年龄

