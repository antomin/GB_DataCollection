from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongo_db = client.books

    def process_item(self, item, spider):
        if spider.name == 'labirintru':
            self.labirintru_pipe(item)
        elif spider.name == 'book24ru':
            self.book24ru_pipe(item)

        collection = self.mongo_db[spider.name]
        collection.insert_one(item)
        return item

    def labirintru_pipe(self, item):
        item['_id'] = 'labirint_' + item['url'].split('/')[-2]
        item['title'] = item['title'].split(': ')[-1]
        if item['price']:
            item['price'] = int(item['price'])
            item['sale_price'] = None
        else:
            item['price'] = int(item['old_price'])
            item['sale_price'] = int(item['sale_price'])
        del item['old_price']
        item['rating'] = float(item['rating'])
        return item

    def book24ru_pipe(self, item):
        item['_id'] = 'book24_' + item['_id'].split(': ')[-1].strip()
        item['title'] = item['title'].split(': ')[-1].strip()
        if item['old_price']:
            item['sale_price'] = int(item['price'])
            item['price'] = int(item['old_price'].split(' ')[1].replace('\xa0', ''))
        else:
            item['price'] = int(item['price']) if item['price'] is not None else None
            item['sale_price'] = None
        del item['old_price']
        item['rating'] = float(item['rating'].replace(',', '.'))
        return item

