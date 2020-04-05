# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class FuhaokuPipeline(object):
    def __init__(self):

        # 连接服务器
        client = pymongo.MongoClient(host='127.0.0.1',port=27017)
        # 创建数据库
        db = client.Fuhaoku
        # 建立集合
        self.collection = db.hanzi

    def process_item(self, item, spider):

        data = dict(item)
        # print(data)

        self.collection.insert(data)

        return item
