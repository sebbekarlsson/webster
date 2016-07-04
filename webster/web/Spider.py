from bs4 import BeautifulSoup
from requests import Session
from urlparse import urlparse, urljoin
from  more_itertools import unique_everseen
from webster.mongo import db
from webster.models import URLEntry
import time
from requests.exceptions import InvalidSchema, ConnectionError
import threading


class Spider(threading.Thread):
    url = None
    sess = None

    def __init__(self, url):
        print('{} : {}'.format(url, self.get_domain(url)))
        self.url = url
        self.sess = Session()

    def get_domain(self, url):
        parsed_uri = urlparse(url)
        return parsed_uri.netloc

    def get_urls(self, soup):
        urls = []

        tags = soup.find_all(href=True) + soup.find_all(src=True)

        for tag in tags:
            if tag.get('href') is not None:
                if self.url not in tag.get('href'):
                    urls.append(urljoin(self.url, tag.get('href')))
                else:
                    urls.append(tag.get('href'))

            if tag.get('src') is not None:
                if self.url not in tag.get('src'):
                    urls.append(urljoin(self.url, tag.get('src')))
                else:
                    urls.append(tag.get('src'))

        return unique_everseen(urls)


    def start(self):
        try:
            html_doc = self.sess.get(self.url).text
        except (InvalidSchema, ConnectionError):
            db.collections.remove(
                        {
                            'structure': '#URLEntry',
                            'url': self.url
                        }
                    )
            return None

        soup = BeautifulSoup(html_doc, 'html.parser')
        urls = self.get_urls(soup)

        this_existing = db.collections.find_one({
                'structure': '#URLEntry',
                'domain': self.get_domain(self.url),
                'url': self.url
                })
        if this_existing is not None:
            db.collections.update_one({
                    'structure': '#URLEntry',
                    'domain': self.get_domain(self.url),
                    'url': self.url
                    }, {'$set': { 'last_scraped': time.strftime("%Y-%m-%d %H:%M:%S")}})

        for url in urls:
            existing = db.collections.find_one({
                'structure': '#URLEntry',
                'domain': self.get_domain(url)
                })

            if existing is None:
                entry = URLEntry(domain=self.get_domain(url), url=url)
                db.collections.insert_one(entry.export())
