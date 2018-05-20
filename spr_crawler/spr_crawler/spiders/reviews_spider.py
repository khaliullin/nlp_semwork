import csv
import os
import re

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request


class QuotesSpider(scrapy.Spider):
    name = "reviews"
    filename = "urls.txt"
    output_path = "corpus"
    dir_name = "Медцентры1"

    pages = []

    def start_requests(self):
        if not os.path.exists(self.output_path + '/' + self.dir_name):
            os.makedirs(self.output_path + '/' + self.dir_name)

        for line in open(self.filename, 'r'):
            url = line.strip()
            print(url)

            request = scrapy.Request(url=url, callback=self.get_reviews_urls, errback=self.make_new_request)
            yield request

    def get_reviews_urls(self, response):
        html = response.body.decode('windows-1251')

        if len(html) == 0:
            return AttributeError

        urls = re.findall('www.spr.ru/forum_vyvod.php\?id_tema=\d+\\\\', html)
        # print('==============================================================================')

        for url in urls:
            url = 'https://' + url[:-1]
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse, errback=self.make_new_request)

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
        filename = self.output_path + '/' + self.dir_name + '/%s_%s.csv' % (page, positive)

        # with open(filename, 'w') as file:
        #     file.write(html)

        text = self.find_between(html, "отзыв'><span>", "<span style='font-weight:bold;'")
        title = self.find_between(html, "<H1>", "</H1>")
        date = re.search('<span>\d{4}-\d{2}-\d{2} \d{2}:\d{2}</span>', html).group()[6:-7]

        # remove html
        text = BeautifulSoup(text, "lxml").text
        title = BeautifulSoup(title, "lxml").text

        with open(filename, 'w', newline='\n') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([title])
            spamwriter.writerow([text])
            spamwriter.writerow([date])

    def make_new_request(self, failure):
        return scrapy.Request(url=failure.request.url, callback=self.get_reviews_urls, errback=self.make_new_request,
                              dont_filter=True)


