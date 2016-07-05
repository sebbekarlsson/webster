import pymongo
from webster.mongo import db
from webster.models import URLEntry
import string
import random
import urlparse
import os.path


file_extensions = [
        '.zip',
        '.jpg',
        '.jpeg',
        '.png',
        '.gif',
        '.bmp',
        '.tar.gz',
        '.pdf'
        ]

def fetch_url(offset=0):
    urls = list(db.collections.find(
                {
                    'structure': '#URLEntry'
                }
            ).skip(offset).limit(1).sort('last_scraped', pymongo.ASCENDING))

    if len(urls) > 0:
        if urls[0] is not None:
            return urls[0]

    return None


def url_file(url):
    return os.path.splitext(
            os.path.basename(
                urlparse.urlsplit(url).path
                )
            )
