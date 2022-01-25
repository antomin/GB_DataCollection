import scrapy
from scrapy.http import HtmlResponse


class LeroymerlinruSpider(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={kwargs.get('search')}"]

    name = "leroymerlinru"
    allowed_domains = ["leroymerlin.ru"]
    start_urls = ["http://leroymerlin.ru/"]

    def parse(self, response: HtmlResponse):
        print("Hello!")
