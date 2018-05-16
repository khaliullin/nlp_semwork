import csv
import re

import scrapy
from bs4 import BeautifulSoup


class QuotesSpider(scrapy.Spider):
    name = "reviews"
    filename = "urls.txt"

    pages = []

    def start_requests(self):
        for line in open(self.filename, 'r'):
            url = line.strip()
            print(url)

            request = scrapy.Request(url=url, callback=self.get_reviews_urls)
            yield request

    def get_reviews_urls(self, response):
        html = response.body.decode('windows-1251')

        urls = re.findall('www.spr.ru/forum_vyvod.php\?id_tema=\d+\\\\', html)
        print('====================================================================================================')
        for url in urls:
            url = 'https://' + url[:-1]
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def find_between(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    def parse(self, response):
        html = response.body.decode('windows-1251')
        page = response.url.split("=")[-1]

        positive = "1" if re.search("title='Это положительный отзыв'><span>", html) else "0"
        filename = 'corpus/%s_%s.csv' % (page, positive)

        text = self.find_between(html, "отзыв'><span>", "<span style='font-weight:bold;'")
        title = self.find_between(html, "<H1>", "</H1>")

        text = BeautifulSoup(text, "lxml").text

        with open(filename, 'w', newline='\n') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([title])
            spamwriter.writerow([text])


