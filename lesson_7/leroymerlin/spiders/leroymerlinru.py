import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from leroymerlin.items import LeroymerlinItem


class LeroymerlinruSpider(scrapy.Spider):
    name = "leroymerlinru"
    allowed_domains = ["leroymerlin.ru"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@data-qa-product]/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath("_id", "//span[@slot='article']/@content")
        loader.add_value("url", response.url)
        loader.add_xpath("title", "//h1/text()")
        loader.add_xpath("price", "//uc-pdp-price-view[@slot='primary-price']/meta[@itemprop='price']/@content")
        loader.add_xpath("images", "//img[@alt='product image']/@src")
        loader.add_xpath("char_list", "//dt[@class='def-list__term']/text()")
        loader.add_xpath("char_values_list", "//dd[@class='def-list__definition']/text()")
        yield loader.load_item()
