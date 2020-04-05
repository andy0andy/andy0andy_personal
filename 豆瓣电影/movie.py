import requests
import json
import time
import threading
import queue


class ThreadCrawl(threading.Thread):
    def __init__(self,threadName,func):
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.func = func

    def run(self):
        print("start->%s" % self.threadName)
        self.func()
        print("end->%s" % self.threadName)


def worker():
    while not pageNum.empty():
        pagenum = pageNum.get()
        js = get_one(pagenum)
        for item in get_data(js):
            write_to_file(f, item)

        print("进度->{.2f}%".format(pagenum*100/499))



def get_one(pagenum):
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=热门&page_limit=20&page_start=" + str(pagenum)

    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding

    if response.status_code == 200:
        # print(response.json())
        return response.json()
    else:
        return None

def get_data(js):
    subjects = js['subjects']

    for subject in subjects:
        item = {
            'rate':subject['rate'],
            'title':subject['title'],
            'url':subject['url'],
            'cover':subject['cover']
        }

        # print(item)
        yield item

def write_to_file(f,item):
    with lock:
        f.write(json.dumps(item,ensure_ascii=False) + '\n')


def main():

    threadcrawl = ['爬虫1号','爬虫2号','爬虫3号','爬虫4号','爬虫5号']
    threadlist = []

    for threadName in threadcrawl:
        thread = ThreadCrawl(threadName,worker)
        thread.start()
        threadlist.append(thread)


    for thread in threadlist:
        thread.join()


if __name__ == '__main__':
    start = time.time()

    pageNum = queue.Queue(500)
    for i in range(500):
        pageNum.put(i)

    lock = threading.Lock()

    f = open("douban-Movie.json", 'a', encoding='utf-8')

    main()

    f.close()

    end = time.time()
    print("OK")
    print("耗时：%.2f"%(end-start))