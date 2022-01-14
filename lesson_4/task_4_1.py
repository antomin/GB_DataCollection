"""
Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости. Для
парсинга использовать XPath. Структура данных должна содержать:
- название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
Сложить собранные новости в БД
Минимум один сайт, максимум - все три
"""

from datetime import datetime

import requests
from lxml import html
from pymongo import MongoClient

# db params
client = MongoClient("127.0.0.1", 27017)
db = client["news"]
lenta_news_collection = db.lenta_news
mail_news_collection = db.mail_news

# request params
lenta_url = "https://lenta.ru/"
mai_url = "https://news.mail.ru/"
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
}

# lenta.ru scraper
responce = requests.get(lenta_url, headers=header)
dom = html.fromstring(responce.text)
news_list = dom.xpath("//div[contains(@class, 'topnews__column')]//a[contains(@class, '_topnews')]")

for news in news_list:
    news_doc = {
        "source": "lenta.ru",
        "title": news.xpath("./div/*[contains(@class, '__title')]/text()")[0],
        "url": news.xpath("./@href")[0]
        if "https:/" in news.xpath("./@href")[0]
        else lenta_url + news.xpath("./@href")[0],
        "time": str(datetime.now().date()) + " " + news.xpath(".//time/text()")[0],
    }

    lenta_news_collection.insert_one(news_doc)

# news.mail.ru scraper
responce = requests.get(mai_url, headers=header)
dom = html.fromstring(responce.text)
news_urls = dom.xpath("//a[contains(@class, '-topnews__item')]/@href | //li[not(contains(@class, 'hidden'))]/a/@href")

for url in news_urls:
    responce = requests.get(url, headers=header)
    url_dom = html.fromstring(responce.text)
    news_doc = {
        "source": url_dom.xpath("//div[@data-news-id]//span[@class='link__text']/text()")[0],
        "title": url_dom.xpath("//h1")[0],
        "url": url,
        "time": url_dom.xpath("//span[@datetime]/@datetime")[0],
    }

    mail_news_collection.insert_one(news_doc)
