import random
import time
from loguru import logger
import pymongo

import pages
import comments


NUM = 100



cli = pymongo.MongoClient(host='175.24.50.215')
db = cli['JD']


if __name__ == '__main__':
    kw = '手机'

    # True：请求服务端，下载列表页并返回商品列表
    # False：加载本地html，返回商品列表
    dl = False

    for i in range(NUM):
        for item in pages.page(kw,i,dl):

            # 封面信息获取
            WriteResult = db['cover'].insert_one(item)

            if not bool(WriteResult):
                logger.debug(f"{id},goodscover")



            comments.run(item['id'])



        logger.info(f'{kw}_{i}.html ok')

        if dl:
            time.sleep(random.random())



        # break
