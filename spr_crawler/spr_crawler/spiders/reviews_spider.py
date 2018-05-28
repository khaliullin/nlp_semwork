import csv
import os
import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request


class ReviewsSpider(scrapy.Spider):
    """
    Создает папку с указанным названием dir_name и записывает в нее
    все отзывы, полученные по ссылкам из файла reviews.txt

    Формат отзывов - csv (Заголовок, текст, дата).
    В названии содержится id отзыва и 0/1 (негативный/позитивный)
    """
    dir_name = 'Медцентры1'
    output_path = "corpus"

    name = "reviews"
    filename = "urls.txt"
    pages = []

    def start_requests(self):
        # создаем папку для отзывов
        if not os.path.exists(self.output_path + '/' + self.dir_name):
            os.makedirs(self.output_path + '/' + self.dir_name)

        # отправляем запросы на получение отзывов по ссылкам из urls.txt
        for line in open(self.filename, 'r'):
            url = line.strip()
            yield scrapy.Request(url=url, callback=self.get_reviews_urls, errback=self.make_new_request)

    def get_reviews_urls(self, response):
        html = response.body.decode('windows-1251')

        # отправляем новый запрос, если IP заблокирован и в ответ приходит пустая страница
        if len(html) == 0:
            return scrapy.Request(url=response.url, callback=self.get_reviews_urls, errback=self.make_new_request,
                                 dont_filter=True)

        # поиск ссылки на отзыв
        urls = re.findall('www.spr.ru/forum_vyvod.php\?id_tema=\d+\\\\', html)

        for url in urls:
            url = 'https://' + url[:-1]
            # отправляем запрос по ссылке на отзыв
            yield scrapy.Request(url=url, callback=self.parse, errback=self.make_new_request_parse)

    def parse(self, response):
        # Содержимое страницы с отзывом
        html = response.body.decode('windows-1251')

        # отправляем новый запрос, если IP заблокирован и в ответ приходит пустая страница
        if len(html) == 0:
            return scrapy.Request(url=response.url, callback=self.parse, errback=self.make_new_request_parse,
                                 dont_filter=True)

        # берем id отзыва из url
        review_id = response.url.split("=")[-1]

        is_positive = "1" if re.search("title='Это положительный отзыв'><span>", html) else "0"

        # создаем имя файла
        filename = self.output_path + '/' + self.dir_name + '/%s_%s.csv' % (review_id, is_positive)

        # достаем заголовок, текст и дату отзыва
        title = self.find_between(html, "<H1>", "</H1>")
        text = self.find_between(html, "отзыв'><span>", "<span style='font-weight:bold;'")
        date = re.search('<span>\d{4}-\d{2}-\d{2} \d{2}:\d{2}</span>', html).group()[6:-7]

        # Очищаем заголовок и текст отзыва от html тегов
        text = BeautifulSoup(text, "lxml").text
        title = BeautifulSoup(title, "lxml").text

        # записываем отзыв в файл csv
        with open(filename, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([title])
            writer.writerow([text])
            writer.writerow([date])

    def make_new_request(self, failure):
        # отправка нового запроса при возврате ошибки
        return scrapy.Request(url=failure.request.url, callback=self.get_reviews_urls, errback=self.make_new_request,
                              dont_filter=True)

    def make_new_request_parse(self, failure):
        # отправка нового запроса при возврате ошибки
        return scrapy.Request(url=failure.request.url, callback=self.parse, errback=self.make_new_request_parse,
                              dont_filter=True)

    @staticmethod
    def find_between(s, first, last):
        """
        Возвращает подстроку в строке между указанными символами
        """
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
