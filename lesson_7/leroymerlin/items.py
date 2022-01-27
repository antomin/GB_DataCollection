import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def value_correction(value: str):
    try:
        value = value.replace(",", ".")
        value = float(value)
    except:
        value = value.strip()
    return value


def get_max_resolution_img(value: str):
    return value.replace("w_1200,h_1200", "w_2000,h_2000")


class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(value_correction))
    images = scrapy.Field(input_processor=MapCompose(get_max_resolution_img))
    specifications = scrapy.Field()
    char_list = scrapy.Field()
    char_values_list = scrapy.Field(input_processor=MapCompose(value_correction))
