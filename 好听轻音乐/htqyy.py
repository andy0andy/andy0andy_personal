# 好听轻音乐

import requests
import time
from lxml import etree
import queue
import threading

# 获得爬取一页的内容，返回一个文本
def get_one_page(url):

    headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    try:
        response = requests.get(url,headers=headers)
        response.encoding = response.apparent_encoding

        return response.text
    except:
        return None


# 获取一页所有歌,返回一个字典，{sid,title}
def get_songs(text):

    item = {}

    html = etree.HTML(text)

    try:
        a_s = html.xpath("//span[@class='title']/a")
        for a in a_s:
            item['sid'] = a.xpath("./@sid")[0]
            item['title'] = a.xpath("./@title")[0]

            # print(item)
            yield item
    except:
        return None




# 下载歌曲
def write_one_song(item):
    try:
        with open("songs/{}.mp3".format(item['title']),'wb') as f:
            url = "http://f2.htqyy.com/play7/" + item['sid'] + "/mp3/3"

            song = requests.get(url)
            f.write(song.content)

            print("\r{} ok".format(item['title']),end="")
    except:
        return None




# 爬取所有页
def get_all_page(url_str):

    pageIndex = 1

    while True:
        print("\r当前页：{}".format(pageIndex),end="")

        url = url_str.format(pageIndex)

        text = get_one_page(url)

        # 尾页处理
        # 有些问题待优化
        if text is None:
            break
        else:
            pageIndex += 1

            # 下载歌曲
            for item in get_songs(text):
                write_one_song(item)
                time.sleep(0.5)
                print()

        time.sleep(2)

    print()




class MyThread(threading.Thread):
    def __init__(self,func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()


def worker():
    while not q.empty():
        url = q.get()
        # 爬取 一条url 歌曲
        get_all_page(url)

        time.sleep(1)


def main():
    threads = []

    url_list = [
        "http://www.htqyy.com/top/musicList/hot?pageIndex={}&pageSize=20",
        "http://www.htqyy.com/top/musicList/new?pageIndex={}&pageSize=20",
        "http://www.htqyy.com/top/musicList/recommend?pageIndex={}&pageSize=20",
        "http://www.htqyy.com/genre/musicList/1?pageIndex={}&pageSize=20&order=hot",
        "http://www.htqyy.com/genre/musicList/3?pageIndex={}&pageSize=20&order=hot",
        "http://www.htqyy.com/genre/musicList/5?pageIndex={}&pageSize=20&order=hot",
    ]

    # url入队列
    for url in url_list:
        q.put(url)


    for i in range(threadNum):
        t = MyThread(worker)
        t.start()
        threads.append(t)


    for t in threads:
        t.join()



if __name__ == '__main__':
    q = queue.Queue()
    threadNum = 3

    start = time.time()
    main()
    end = time.time()

    print("共用时间：{}".format(end-start))
    print("OK")