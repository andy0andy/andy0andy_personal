import requests
import re
import time
import csv

def get_Html(url):
    cookie = "thw=cn; enc=Idt2xLNpC8VEhvzhCzXVJHL36N6n%2Bi2uTsk2aNdkBUIbsMGrKiTwoydK76sDozjeQKuMIfWXDVSE8GZBBfJNUw%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; cna=xW/4FlDd9lgCAbZgwCHnZa1F; lgc=%5Cu8377%5Cu5305%5Cu9F13%5Cu9F13%5Cu5411%5Cu6211%5Cu5F00; tracknick=%5Cu8377%5Cu5305%5Cu9F13%5Cu9F13%5Cu5411%5Cu6211%5Cu5F00; tg=0; sgcookie=EtJHkh8A5EvgjhkPF8srR; uc3=id2=UU8INKksuoXoOg%3D%3D&nk2=2WkphiEGsBw9moIiFNQ%3D&lg2=WqG3DMC9VAQiUQ%3D%3D&vt3=F8dBxdAXvWGfIj52Sso%3D; uc4=nk4=0%4024%2BaeeH4zeLnifV9C1A%2FIwSbDpFydSJeOg%3D%3D&id4=0%40U22PEY2W%2F5F77IolZXf2XT34zvA4; _cc_=URm48syIZQ%3D%3D; tfstk=cla1BdTk9dv_s5vxRR1Eb1UifduAZ28IteDU1kQ5W9KAYWP1iLYrFXRi1pTK2X1..; miid=768858522029824354; mt=ci=-1_0; v=0; cookie2=1cf6b07a89e865c7c4541b38baf3990c; t=412c3098eba5ae701abdfdab821b9670; _tb_token_=f09e6e7338553; alitrackid=www.taobao.com; JSESSIONID=3F6C68B16E7B81BAF07C1291A216BCC5; lastalitrackid=blog.csdn.net; uc1=cookie14=UoTUPcqcCt5L1A%3D%3D; isg=BK-vcREDLYZqWimbNHrRA1brPsO5VAN2g_ZtwcE8-p4DEM0SySaQxriJlgAuaNvu; l=eBERoRilQBbvtA_0BO5iqYBNC6QOyIRbzsPyyjNg2IHca6C1Teo-2NQcD7cH7dtjgtfUHetzm21B9dUp5E4dAxDDBexrCyClcxJ6-"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"zh-CN,zh;q=0.9",
        "cache-control":"max-age=0",
        "sec-fetch-dest":"document",
        "sec-fetch-mode":"navigate",
        "sec-fetch-site":"same-origin",
        "sec-fetch-user":"?1",
        "upgrade-insecure-requests":"1"
    }

    # cookies为键值对格式
    cookies = {}
    for c in cookie.split('; '):
        k,v = c.strip().split('=',1)
        cookies[k] = v

    try:
        response = requests.get(url,headers=headers,cookies=cookies)
        response.encoding = response.apparent_encoding

        return response.text

    except:
        print("获取页面失败T.T")
        pass


# 生成器，每次迭代数据
def parse_html(html):
    auctions = re.findall('"auctions":\[(.*)],"recommendAuctions":',html)[0]
    auctions = re.sub('}(,?){"i2iTags":','@',auctions).split('@')
    # print(len(auctions))        # 一页48条数据
    for data in auctions:
        item = {}

        item['nid'] = re.findall('"nid":"(.*?)","category"',data)[0]
        item['pid'] = re.findall('"pid":"(.*?)","title"',data)[0]
        item['title'] = re.sub('\\\\[a-zA-Z0-9 ]*','',re.findall('"title":"(.*?)","raw_title"',data)[0]).replace('/span','')
        item['raw_title'] = re.findall('"raw_title":"(.*?)","pic_url"',data)[0]
        item['detail_url'] = re.findall('"detail_url":"(.*?)","view_price"',data)[0]
        item['view_price'] = re.findall('"view_price":"(.*?)","view_fee"',data)[0]
        item['view_fee'] = re.findall('"view_fee":"(.*?)","item_loc"',data)[0]
        item['item_loc'] = re.findall('"item_loc":"(.*?)","view_sales"',data)[0]
        item['view_sales'] = re.findall('"view_sales":"(.*?)","comment_count"',data)[0]
        item['comment_count'] = re.findall('"comment_count":"(.*?)","user_id"',data)[0]
        item['user_id'] = re.findall('"user_id":"(.*?)","nick"',data)[0]
        item['nick'] = re.findall('"nick":"(.*?)","shopcard"',data)[0]

        # print(item)
        yield item


def download_to_csv(writer,item):
    writer.writerow(item)



def main():
    q = input('请输入需要搜索的商品：')
    page = 5
    count = 1

    with open('taobao-{}.csv'.format(q), 'a+', encoding='utf-8', newline='') as f:
        fieldnames = ['nid', 'pid', 'title', 'raw_title', 'detail_url', 'view_price', 'view_fee', 'item_loc',
                      'view_sales', 'comment_count', 'user_id', 'nick']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(page):
            url = "https://s.taobao.com/search?q={0}&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=0&ntoffset=6&p4ppushleft=1%2C48&s={1}".format(q,i*44)

            html = get_Html(url)
            # print(html)

            for item in parse_html(html):
                download_to_csv(writer,item)
                count += 1
                print("正在全力下载中-- {0:.1f}%-[{1}/{2}]".format(count*100/(page*48),count,page*48),end='\r')
            print()

            time.sleep(1)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()

    print("耗时：{:.2f}".format(end-start))
    print('OK')