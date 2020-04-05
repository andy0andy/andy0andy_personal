from scrapy import cmdline

def runcrwal():
    cmdline.execute("scrapy crawl taobao".split())


if __name__ == '__main__':
    runcrwal()