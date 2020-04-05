# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.files import FilesPipeline

class HtqyyPipeline(FilesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        return scrapy.Request(item['sid'],meta={"sname":item['sname']})

    def file_path(self, request, response=None, info=None):
        filename = u"songs/{}.mp3".format(request.meta['sname'])

        return filename



