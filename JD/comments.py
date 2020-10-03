import requests
import time
import random
import json
import pymongo
from lxml import etree
from fake_useragent import UserAgent
import re
from loguru import logger

import proxy



NUM = 100

ua = UserAgent()

cli = pymongo.MongoClient(host='175.24.50.215')
db = cli['JD']

log = logger.add('err_log.log',enqueue=True)

proxies_list = proxy.run()


def info(url):
    headers = {
        'User-Agent':ua.random
    }

    response = requests.get(url,headers=headers)

    html = etree.HTML(response.text,etree.HTMLParser())

    goods_info = html.xpath("//ul[@class='parameter2 p-parameter-list']/li/text()")

    return goods_info



def comment(id,page):

    url = "https://club.jd.com/comment/productPageComments.action"

    params = {
        "callback": "fetchJSON_comment98",
        "productId": id,
        "score": "0",
        "sortType": "5",
        "page": page,
        "pageSize": "10",
        "isShadowSku": "0",
        "fold": "1",
    }

    headers = {
        'User-Agent':ua.random
    }

    goods_url = f"https://item.jd.com/{id}.html"
    goodsInfo = info(goods_url)

    r = requests.get(url,params=params,headers=headers,timeout=30)
    text = r.text

    try:
        text = re.findall("fetchJSON_comment98\((.+?)\)",text)[0]

        fetchJSON_comment98 = json.loads(text)

        # 获取总评，好评，标签等信息
        if page == 0:
            productCommentSummary = fetchJSON_comment98['productCommentSummary']
            commentCount = productCommentSummary['commentCount']  # 总评论
            defaultGoodCount = productCommentSummary['defaultGoodCount']  # 好评

            hotCommentTagStatistics = fetchJSON_comment98['hotCommentTagStatistics']

            hotTags = []
            for hot_tag in hotCommentTagStatistics:
                tags = {}
                tags['name'] = hot_tag['name']
                tags['count'] = hot_tag['count']

                hotTags.append(tags)

            data = {
                'id': id,
                'commentCount': commentCount,
                'defaultGoodCount': defaultGoodCount,
                'hotTags': hotTags,
                'goodsInfo': goodsInfo
            }

            # 保存mongo
            WriteResult = db['goodsInfo'].insert_one(data)

            if not bool(WriteResult):
                logger.debug(f"{id},goodsInfo")

        # 获取评论
        comments = fetchJSON_comment98['comments']

        contents = []
        for cm in comments:
            contents.append({
                'content':cm['content'],
                'usefulVoteCount':cm['usefulVoteCount']
            })

        data = {
            'id': id,
            'page': page,
            'comments': contents
        }

        # 保存mongo
        WriteResult = db['comments'].insert_one(data)
        if not bool(WriteResult):
            logger.debug(f"{id},comments,{page}")

        print('comments: ',id, page, 'ok')

        # 翻页，边界值
        maxPage = int(fetchJSON_comment98['maxPage'])

    except Exception as e:
        maxPage = int(re.findall('"maxPage":(.+?),',text)[0])


    if page < maxPage:
        page += 1

        time.sleep(random.random())
        comment(id,page)
    else:
        return





def run(id):

    try:
        comment(id,0)
    except Exception as e:
        logger.error(f"{id},{str(e)}")
        print('comments.py: ',e)




if __name__ == '__main__':

    run('100006583459')

