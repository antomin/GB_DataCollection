import scrapy
from scrapy.http import HtmlResponse


class LeroymerlinruSpider(scrapy.Spider):
    name = "leroymerlinru"
    allowed_domains = ["leroymerlin.ru"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://leroymerlin.ru/search/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@data-qa-product]/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        article = response.xpath("//span[@slot='article']/@content").get()
        title = response.xpath("//h1/text()").get()
        price = response.xpath("//uc-pdp-price-view[@slot='primary-price']/meta[@itemprop='price']/@content").get()
        img = response.xpath("//img[@alt='product image']/@src").getall()
        pass
