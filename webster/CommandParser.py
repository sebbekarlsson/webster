from webster.web.Spider import Spider
from webster.mongo import db
from webster.models import URLEntry
import pymongo
import threading
import json
from terminaltables import AsciiTable


def deploy_spider(spider):
    return spider.start()

def find(args, conn):
    if len(args) > 0:
        if str(args[0]) != 'tld':
            urls = list(db.collections.find(
                    {
                        'structure': '#URLEntry',
                        'domain': {'$regex': '{}'.format(str(args[0]))}
                    }
                    ).sort('last_scraped', pymongo.DESCENDING))
        else:
            urls = list(db.collections.find(
                    {
                        'structure': '#URLEntry',
                        'tld': str(args[1])
                    }
                    ).sort('last_scraped', pymongo.DESCENDING))

        if urls is not None:
            if urls[0] is not None:
                table_data = [
                    ['domain', 'scraped'],
                ]

                for url in urls:
                    if len(url['domain']) > 120:
                        url['domain'] = url['domain'][0:120]
                        
                    entry = [url['domain'], url['last_scraped']]

                    if entry[0] not in [e[0] for e in table_data]:
                        table_data.append(entry)

                table = AsciiTable(table_data)
                output = table.table + "\n" + "Rows: {}".format(len(table_data)-1)

        return conn.send(output.encode('utf-8').strip())

def urlfind(args, conn):
    if len(args) > 0:
        if str(args[0]) != 'tld':
            urls = list(db.collections.find(
                    {
                        'structure': '#URLEntry',
                        'url': {'$regex': '{}'.format(str(args[0]))}
                    }
                    ).sort('last_scraped', pymongo.DESCENDING))
        else:
            urls = list(db.collections.find(
                    {
                        'structure': '#URLEntry',
                        'tld': str(args[1])
                    }
                    ).sort('last_scraped', pymongo.DESCENDING))

        if urls is not None:
            if urls[0] is not None:
                table_data = [
                    ['url', 'scraped'],
                ]

                for url in urls:
                    if len(url['url']) > 120:
                        url['url'] = url['url'][0:120]
                        
                    entry = [url['url'], url['last_scraped']]
                    table_data.append(entry)

                table = AsciiTable(table_data)
                output = table.table + "\n" + "Rows: {}".format(len(table_data)-1)

        return conn.send(output.encode('utf-8').strip())

def rm(args, conn):
    if len(args) > 0:
        res = db.collections.delete_many({
                'structure': '#URLEntry',
                'domain': {'$regex': '{}'.format(str(args[0]))}
            })

        if res is not None:
            return conn.send(b'{} documents deleted'.format(res.deleted_count))
        else:
            return conn.send(b'Unable to perform action')

def scrape_date_reset(args, conn):
    res = db.collections.update_many(
        {
            'structure': '#URLEntry'
        },
        {
            '$set': {
                'last_scraped': '0-0-0 0:0:0'
            }   
        }
    )

    if res is not None:
        return conn.send(b'{} documents where updated'.format(res.matched_count))
    else:
        return conn.send(b'Unable to update documents')

class CommandParser(object):
    def parse(self, data, conn):
        if data is None or data == '':
            return conn.send(u'...')

        try:
            args = data.split(' ')
            command = args[0]
            args.pop(0)
        except Exception as e:
            return conn.send(str(e))

        if command == 'SERVER->QUIT':
            return conn.send(u'TERMINATING')
            conn.close()
            quit()

        if command == 'find':
            return find(args, conn)

        if command == 'urlfind':
            return urlfind(args, conn)

        if command == 'rm':
            return rm(args, conn)

        if command == 'scrape_date_reset':
            return scrape_date_reset(args, conn)

        if command == 'spider':
            if len(args) > 0:
                spider = Spider(args[0])

                t = threading.Thread(target=deploy_spider, args=(spider, ))
                t.daemon = True
                t.start()

                return conn.send(u'DEPLOYED SPIDER WITH URL: {}'.format(spider.url).encode('utf-8').strip())

        conn.send('Unknown Command')
