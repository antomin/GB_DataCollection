from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class LeroymerlinPipeline:
    def process_item(self, item, spider):
        return item


class LeroymerlinImagesPipiline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["images"]:
            for img in item["images"]:
                try:
                    yield Request(img)
                except Exception as error:
                    print(error)

    def item_completed(self, results, item, info):
        item["images"] = [el[1] for el in results if el[0]]
        return item
