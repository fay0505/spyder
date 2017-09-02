# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class PeoplePaperPipeline(object):

    def open_spider(self, spider):
        self.f = open("PeoplePaperNewsInfo.txt", 'w')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        try:
            line = str(dict(item)) + '\n'
            self.f.write(line)
        except:
            pass
        return item


class MongoPipeline(object):

    def __init__(self):

        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        client = pymongo.MongoClient(host=host, port=port)
        dbname = settings['MONGODB_DBNAME']
        tdb = client[dbname]
        self.post = tdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):

        self.post.update( dict(item))
        return item

