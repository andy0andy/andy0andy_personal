# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class ImgspiderPipeline(ImagesPipeline):
    # def process_item(self, item, spider):
    #     return item

    def get_media_requests(self, item, info):
        for img in item['imgurl']:
            yield scrapy.Request(img,meta={'dirname':item['imgdirname']})


    def file_path(self, request, response=None, info=None):
        # 获取 meta 传进参数作为文件名
        # print(request.meta['dirname'])
        dirname = request.meta['dirname']

        # 从 url 获取到字符串，以 / 为分隔符分割url地址，截取最后一段数字作为每个图片名
        # print(request.url.split('/')[-1])
        imgname = request.url.split('/')[-1]

        # 文件储存的关键
        filename = u"{}/{}".format(dirname,imgname)
        return filename

