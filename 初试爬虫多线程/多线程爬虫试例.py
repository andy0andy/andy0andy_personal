from queue import Queue
import threading

class ThreadCrawl(threading.Thread):
    def __init__(self,threadName,crawl):
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.crawl = crawl


    def run(self):
        print("start: {}".format(self.threadName))
        self.crawl()
        print("end: {}".format(self.threadName))


def worker():
    while not urlQueue.empty():
        print("我是一只爬虫-%d" % urlQueue.get())


def main():

    threadcrawl = ['爬虫线程1号','爬虫线程2号','爬虫线程3号']
    threadlist = []

    for threadName in threadcrawl:
        thread = ThreadCrawl(threadName,worker)
        thread.start()
        threadlist.append(thread)


    for thread in threadlist:
        thread.join()




if __name__ == '__main__':
    urlQueue = Queue()
    for i in range(100):
        urlQueue.put(i)

    main()
    print("OK!!!")

