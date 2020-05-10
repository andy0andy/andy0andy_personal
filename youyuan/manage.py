from scrapy import cmdline

def runcrawl():
    cmdline.execute("scrapy crawl mm18-0 -o mm18-0.csv".split())


if __name__ == '__main__':
    runcrawl()