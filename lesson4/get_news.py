import requests
from pprint import pprint
from lxml import html
from uuid import uuid4
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)


def yandex_news():
    pass


def mail_news():
    url = 'https://news.mail.ru/'
    db = client['mail_news']
    news_list = []
    collection = db.news_collection
    collection.drop()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36'}
    response = requests.get(url, headers=headers).text
    root = html.fromstring(response)
    news = root.xpath("//div[@class='daynews__item daynews__item_big'] | //div[@class='daynews__item hidden_small'] | "
                      "//div[@class='daynews__item'] | //span[@class='list__text'] | //span[@class='cell'] | "
                      "//li[@class='list__item']")
    for item in news:
        try:
            name = item.xpath(".//a/span/span/text()")[0]
        except IndexError:
            try:
                name = item.xpath(".//a/span/text()")[0]
            except IndexError:
                name = item.xpath(".//a[@class='list__text']/text()")[0]

        news_element = {
            'source': url,
            'time_update': datetime.now(),
            'name': name,
            'link': item.xpath(".//a/@href")[0]
        }
        news_list.append(news_element)
    collection.insert_many(news_list)


def lenta_news():
    url = 'https://lenta.ru/'
    db = client['lenta_news']
    news_list = []
    collection = db.news_collection
    collection.drop()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.110 Safari/537.36'}
    response = requests.get(url, headers=headers).text
    root = html.fromstring(response)
    news_type_main = root.xpath("//a[@class='card-mini _compact'] | //a[@class='card-mini _topnews'] | "
                                "//a[@class='card-mini _longgrid'] | //a[@class='card-big _longgrid']")
    for item in news_type_main:
        news_element = {
            'source': url,
            'time_update': datetime.now(),
            'name': item.xpath(".//div/span/text()")[0],
            'link': item.xpath(".//@href")[0]
        }
        news_list.append(news_element)
    collection.insert_many(news_list)


mail_news()
lenta_news()
