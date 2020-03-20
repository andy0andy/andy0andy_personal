# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class NetbianPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        for i in range(len(item['imgurl'])):
            imgurl = "http://pic.netbian.com" + item['imgurl'][i]

            yield scrapy.Request(imgurl,meta={'imgname':item['imgname'][i],'dirname':item['dirname']})



    def file_path(self, request, response=None, info=None):

        imgname = request.meta['imgname'].strip() + '.jpg'
        dirname = request.meta['dirname']

        filename = u"{}/{}".format(dirname,imgname)

        return filename