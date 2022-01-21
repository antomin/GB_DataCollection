import scrapy
from scrapy.http import HtmlResponse
import requests
from bookparser.items import BookparserItem


class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5']

    page = 2

    def parse(self, response: HtmlResponse):
        next_page = f'https://book24.ru/search/page-{self.page}/?q=%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5'
        if requests.get(next_page).ok:
            yield response.follow(next_page, callback=self.parse)
            self.page += 1
        links = response.xpath("//article[@class='product-card']//a[@class='product-card__name smartLink']/@href")
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        _id = response.xpath("//p[@class='product-detail-page__article']/text()").get()
        url = response.url
        title = response.xpath("//h1/text()").get()
        authors = response.xpath("//div[contains(@class, 'product-detail-page__product-characteristic')]//a[contains(@href, '/author/')]/@title").getall()
        price = response.xpath("//meta[@itemprop='price']/@content").get()
        old_price = response.xpath("//span[@class='app-price product-sidebar-price__price-old']/text()").get()
        rating = response.xpath("//span[@class='rating-widget__main-text']/text()").get()

        yield BookparserItem(_id=_id, url=url, title=title, authors=authors, price=price, old_price=old_price, rating=rating)