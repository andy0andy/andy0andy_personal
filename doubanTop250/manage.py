from scrapy import cmdline

def main():
    cmdline.execute("scrapt crawl top250".split())


if __name__ == '__main__':
    main()