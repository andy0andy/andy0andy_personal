from scrapy import cmdline

def runcrawl():
    cmdline.execute("scrapy crawl htqyy".split())


if __name__ == '__main__':
    runcrawl()