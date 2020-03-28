import queue
import threading
import time


class MyTread(threading.Thread):
    def __init__(self,func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()



def worker():
    while not q.empty():
        item = q.get()
        print("processing: ",item)
        time.sleep(1)


def main():
    threads = []
    for i in range(100):
        q.put(i)

    for i in range(threadNum):
        # 创建一个线程，并执行
        thread = MyTread(worker)
        thread.start()
        threads.append(threads)

    for thread in threads:
        thread.join()




if __name__ == '__main__':
    q = queue.Queue()
    threadNum = 3
    main()