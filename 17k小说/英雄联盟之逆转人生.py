import requests
from pyquery import PyQuery as pq
import time
import os

def get_article_list(url):
    book = requests.get(url,verify=False)
    book.encoding = book.apparent_encoding

    if book.status_code == 200:
        doc = pq(book.text)
        item = {}

        item['btitle'] = doc(".Title").text() + "-" + doc(".Author a").text()
        item['binfo'] = []

        volume = doc(".Volume dd a").items()

        for a in volume:
            ainfo = {}
            ainfo['atitle'] = a(".ellipsis").text()
            ainfo['aurl'] = "https://www.17k.com" + a.attr('href')

            item['binfo'].append(ainfo)

        # print(item)
        return item
    else:
        return None


def get_article(url):
    response = requests.get(url,verify=False)
    response.encoding = response.apparent_encoding

    doc = pq(response.text)

    ps = doc(".p p")
    article = ""

    for p in ps.items():
        article += p.text() + '\n'

    # print(article)
    return article


def get_download(item):
    count = 1

    binfo = item['binfo']
    if not os.path.exists(item['btitle']):
        os.mkdir(item['btitle'])
    for article in binfo:
        count += 1
        if count > 50:
            break

        try:
            with open("{}/{}.txt".format(item['btitle'],article['atitle']),'w',encoding='utf-8') as f:
                article = get_article(article['aurl'])
                f.write(article)

                time.sleep(0.5)
            print("{0} ok".format(article['atitle']))
        except:
            continue





def main():
    url = "https://www.17k.com/list/1250978.html"
    item = get_article_list(url)
    get_download(item)

    # get_article("https://www.17k.com/chapter/1250978/20353971.html")

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()

    print("耗时：%.2f" % (end-start))
    print("OK!!!")