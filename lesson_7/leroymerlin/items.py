import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def price_to_float(value: str):
    try:
        value = float(value)
    except:
        value = None
    return value


def get_max_resolution_img(value: str):
    return value.replace("w_1200,h_1200", "w_7000,h_7000")


class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_to_float))
    images = scrapy.Field()  # (input_processor=MapCompose(get_max_resolution_img))
