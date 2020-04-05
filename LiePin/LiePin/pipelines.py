# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from LiePin.items import LiepinItem

class LiepinPipeline(object):
    def __init__(self):
        self.f = open('liepin-python.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        self.f.write(json.dumps(dict(item),ensure_ascii=False) + '\n')
        # print("->",spider.name)
        # print("->",isinstance(item,LiepinItem))
        return item

    def close_spider(self,spider):
        self.f.close()