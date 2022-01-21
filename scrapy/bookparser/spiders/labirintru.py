import scrapy

from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        url = response.url
        title = response.xpath("//h1/text()").get()
        authors = response.xpath("//a[@data-event-label='author']/text()").getall()
        price = response.xpath("//span[@class='buying-price-val-number']/text()").get()
        old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        sale_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()

        yield BookparserItem(url=url, title=title, authors=authors, price=price, old_price=old_price, sale_price=sale_price, rating=rating)
