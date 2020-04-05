import requests
from lxml import etree
import json
import time
import queue
import threading



def get_one_page(pageNum):
    url = "https://www.qiushibaike.com/8hr/page/" + str(pageNum) + "/"

    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    try:
        response = requests.get(url,headers=headers,verify=False)
        response.encoding = 'utf-8'
    except:
        pass

    if response.status_code == 200:
        return response.text
    else:
        return None


def get_items(text):
    html = etree.HTML(text)

    nodes = html.xpath("//li[contains(@id,'qiushi_tag')]")

    try:
        for node in nodes:
            item = {
                "title":node.xpath("./div/a/text()")[0],
                'img':"https://" + node.xpath("./a/img/@src")[0],
                'author':node.xpath("./div/div/a/span/text()")[0]
            }

            # print(item)
            yield item
    except:
        pass


def download_item(item):
    with lock:

        # print(item)

        f.write(json.dumps(item,ensure_ascii=False) + '\n')




class ThreadCrawl(threading.Thread):
    def __init__(self,threadName,worker):
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.worker = worker

    def run(self):
        print("start-{}".format(self.threadName))
        self.worker()
        print("end-{}".format(self.threadName))


def worker():
    while not pageNum.empty():
        num = pageNum.get()
        print("Page to {}".format(num))

        text = get_one_page(num)
        items = get_items(text)
        for item in items:
            download_item(item)

        time.sleep(1)


def main():
    # 用线程，6s左右
    threadcrawl = ['爬虫线程1号','爬虫线程2号','爬虫线程3号','爬虫线程4号']
    threadlist = []
    for threadNmae in threadcrawl:
        thread = ThreadCrawl(threadNmae,worker)
        thread.start()
        threadlist.append(thread)

    for thread in threadlist:
        thread.join()


    # 不要用线程，14s左右
    # for num in range(1,21):
    #     text = get_one_page(num)
    #     items = get_items(text)
    #     for item in items:
    #         download_item(item)



if __name__ == '__main__':
    pageNum = queue.Queue()
    for i in range(1,21):
        pageNum.put(i)

    lock = threading.Lock()
    f = open("qsbk.json",'a',encoding='utf-8')

    start = time.time()
    main()
    end = time.time()
    print("耗时：",end-start)
    print("OK")

    f.close()