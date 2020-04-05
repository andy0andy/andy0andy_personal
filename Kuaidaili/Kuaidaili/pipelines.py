# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class KuaidailiPipeline(object):
    def __init__(self):
        csvheader = ['proxy','position','speed']
        self.f = open("快代理-国内高匿代理.csv",'a+',encoding='utf-8',newline="")
        self.writer = csv.DictWriter(self.f,csvheader)
        self.writer.writeheader()

    def process_item(self, item, spider):

        self.writer.writerow(dict(item))

        return item


    def close_spider(self,spider):
        self.f.close()
