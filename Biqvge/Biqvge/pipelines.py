# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class BiqvgePipeline(object):
    def process_item(self, item, spider):

        with open("Books/剑道独尊/{}.txt".format(item['bookname']),'w',encoding="utf-8") as f:
            f.write(item['content'])


        return item
