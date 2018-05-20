import re

import scrapy


class QuotesSpider(scrapy.Spider):
    """
    Returns urls of institutions by given direction url
    """
    name = "catalogue"
    filename = "directions.txt"
    catalogue = "https://www.spr.ru/all/medtsentri/"

    def start_requests(self):
        f = open(self.filename, 'w')
        f.write("")
        request = scrapy.Request(url=self.catalogue, callback=self.parse)
        request.meta['file'] = f
        yield request

    def parse(self, response):
        f = response.meta['file']

        html = response.body.decode('windows-1251')
        matches = re.findall("(a href='//www.spr.ru/all/.+?' title='.*?')", html)

        for match in matches[:-1]:
            part = match.split("' title='")
            url = 'https:' + part[0][8:]
            title = part[1].split(" — ")[0]
            f.write(url + '\t' + title + '\n')

