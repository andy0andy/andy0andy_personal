from scrapy import cmdline

def runcrawl():

    cmdline.execute("scrapy crawl FreeInha".split())


if __name__ == '__main__':
    runcrawl()