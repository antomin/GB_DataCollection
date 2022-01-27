import hashlib

from pymongo import MongoClient
from runner import SEARCH
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class LeroymerlinMongoDBPipeline:
    def __init__(self):
        client = MongoClient("127.0.0.1", 27017)
        self.mongo_db = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_db[SEARCH]
        collection.insert_one(item)
        return item


class LeroymerlinSpecificationsPipeline:
    def process_item(self, item, spider):
        item["specifications"] = dict(zip(item["char_list"], item["char_values_list"]))
        del item["char_list"], item["char_values_list"]
        return item


class LeroymerlinImagesPipiline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["images"]:
            for img in item["images"]:
                try:
                    yield Request(img)
                except Exception as error:
                    print(error)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{SEARCH}/{item['_id']}/{image_guid}.jpg"

    def item_completed(self, results, item, info):
        item["images"] = [el[1] for el in results if el[0]]
        return item
