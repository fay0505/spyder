# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from  scrapy.conf import settings


class JfdailyPipeline(object):

    def open_spider(self, spider):
        self.f = open('NewsInfo.txt', 'a')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        try:
            line = str(dict(item))  + '\n'
            self.f.write(line)
        except:
            pass

        return item


class MongoPipeline(object):

    def __init__(self):

        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        client = pymongo.MongoClient(host=host, port=port)   #获取连接
        dbname = settings['MONGODB_DBNAME']
        tdb = client[dbname]
        self.post = tdb[settings['MONGODB_DOCNAME']]    #创建要操作的集合

    def process_item(self, item, spider):
        self.post.insert(dict(item))
        #self.post.update({"ip":item}, {'$set': {'ip': dict(item)})
        return item