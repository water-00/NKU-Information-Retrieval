# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo.errors import DuplicateKeyError
from pagerank.items import PagerankItem

class PagerankPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
    def __init__(self, local_mongo_host, local_mongo_port, mongo_db):
        self.local_mongo_host = local_mongo_host
        self.local_mongo_port = local_mongo_port
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            local_mongo_host=crawler.settings.get('LOCAL_MONGO_HOST'),
            local_mongo_port=crawler.settings.get('LOCAL_MONGO_PORT'),
            mongo_db=crawler.settings.get('DB_NAME')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.local_mongo_host, self.local_mongo_port)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, PagerankItem):
            self.insert_item(self.db[item.collection], item)
        return item

    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert_one(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            pass