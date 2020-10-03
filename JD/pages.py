import requests
from fake_useragent import UserAgent
from lxml import etree
import os
import re



ua = UserAgent()



# 列表页
url = "https://search.jd.com/Search"


def download_page(text,ki,dl):
    html = etree.HTML(text,etree.HTMLParser())

    if dl:
        with open(os.path.join(os.getcwd(),os.path.join('pages_dir',f"{ki[0]}_{ki[1]}.html")),'w+',encoding='utf-8') as f:
            f.write(etree.tostring(html,encoding='utf-8').decode('utf-8'))
    
    return html



def parse_page(html):

    goodsList = html.xpath("//div[@id='J_goodsList']/ul/li")

    for goods in goodsList:
        item = {}


        item['price'] = goods.xpath(".//div[@class='p-price']//i/text()")[0]
        item['name'] = ''.join(goods.xpath(".//div[@class='p-name p-name-type-2']//em/text()")).replace('\t','').replace('\n','').replace('\r','').replace('\xa0','')
        item['shop'] = ''.join(goods.xpath(".//div[@class='p-shop']//a/text()"))
        item['goods_url'] = 'https:' + ''.join(goods.xpath(".//div[@class='p-img']//a/@href"))
        item['id'] = re.findall('\/(\d+?)\.html$',item['goods_url'])[0]

        # print(item)
        yield item




def page(kw,index,dl):
    headers = {
        'User-Agent':ua.random
    }
   
    params = {
        'keyword': kw,
        'page': 1 + (index - 1) * 2,    # +2
        's': 1 + (index - 1) * 50,   # 50
        'click': 0,
    }
    
    if dl:
        response = requests.get(url,headers=headers,params=params)

        # 下载单个页面，并返回 html
        html = download_page(response.text,[kw,index],dl)

    else:

        html = etree.parse(os.path.join(os.getcwd(),os.path.join('pages_dir',f'{kw}_{index}.html')),parser=etree.HTMLParser())


    for item in parse_page(html):
        print(item)
        yield item







if __name__ == "__main__":
    kw = '手机'
    index = 1
    dl = False    

    item_list = page(kw,index,dl)


