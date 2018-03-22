# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from scrapy.exceptions import DropItem

class MongoPipeline(object):

    collection_name = 'challenges'

    def __init__(self):
        self.mongo_uri = 'mongodb://localhost:27017'
        self.mongo_db = 'tatainnoverse'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].update({'_id' : item['_id']},dict(item), upsert=True)
        return item

class ValidatePipeline(object):
    def process_item(self, item, spider):
        if("http" in item['url'] and 'tatainnoverse' not in item['url']):
            return item
        else:
            raise DropItem()



class CrawlersPipeline(object):
    def process_item(self, item, spider):
        return item
