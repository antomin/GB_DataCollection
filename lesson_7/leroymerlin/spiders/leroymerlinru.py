import scrapy
from scrapy.http import HtmlResponse


class LeroymerlinruSpider(scrapy.Spider):
    name = "leroymerlinru"
    allowed_domains = ["leroymerlin.ru"]
    start_urls = ["http://leroymerlin.ru/"]

    def parse(self, response: HtmlResponse):
        print("Hello!")
