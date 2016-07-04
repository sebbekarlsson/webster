from webster.web.Spider import Spider
from webster.web.extra import fetch_url
import threading


class SpiderNet(object):
    spiders = []

    def __init__(self):
        pass

    def start(self, urls):
        for url in urls:
            spider = Spider(url)
            spider.start()

        try:
            while True:
                spider = Spider(fetch_url()['url'])
                spider.start()
        except KeyboardInterrupt:
            quit()
