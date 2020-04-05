from scrapy import cmdline

def runcrawl():
    cmdline.execute("scrapy crawl Book_jddz".split())



if __name__ == '__main__':
    runcrawl()