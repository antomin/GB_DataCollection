from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_db = client.books

    def process_item(self, item, spider):
        if spider.name == 'labirintru':
            item['_id'] = spider.name + '_' + item['url'].split('/')[-2]
            item['title'] = item['title'].split(': ')[-1]
            if item['price']:
                item['price'] = int(item['price'])
                item['sale_price'] = None
            else:
                item['price'] = int(item['old_price'])
                item['sale_price'] = int(item['sale_price'])
            del item['old_price']
            item['rating'] = round(float(item['rating']), 2)
            # print()
        collection = self.mongo_db[spider.name]
        collection.insert_one(item)

        return item
