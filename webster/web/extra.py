import pymongo
from webster.mongo import db
from webster.models import URLEntry
import string
import random


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
