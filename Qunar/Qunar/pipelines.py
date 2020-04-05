# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv


class QunarPipeline(object):
    def __init__(self):
        csvheader = ['title','level','addr','tip','price']
        self.f = open("广州景区.csv",'a',encoding='utf-8',newline="")
        self.writer = csv.DictWriter(self.f,csvheader)
        self.writer.writeheader()


    def process_item(self, item, spider):

        self.writer.writerow(dict(item))

        return item


    def close_spider(self,spider):
        self.f.close()