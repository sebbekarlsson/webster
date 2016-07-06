from webster.web.Spider import Spider
from webster.web.extra import fetch_url
import threading


class SpiderNet(threading.Thread):
    urls = []

    def __init__(self, urls):
        threading.Thread.__init__(self)
        self.urls = urls
        self.running = True
        self.daemon = True

    def run(self):
        for url in self.urls:
            spider = Spider(url)
            spider.start()

        while self.running:
            spider = Spider(fetch_url()['url'])
            spider.start()
            
        #quit()
