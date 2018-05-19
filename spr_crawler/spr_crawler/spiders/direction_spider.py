import re

import scrapy


class QuotesSpider(scrapy.Spider):
    """
    Returns urls of institutions by given direction url
    """
    name = "direction"
    filename = "institutions.txt"
    direction = "https://www.spr.ru/all/dispanseri-onkologicheskie/"

    def start_requests(self):
        f = open(self.filename, 'w')
        f.write("")
        request = scrapy.Request(url=self.direction, callback=self.parse)
        request.meta['file'] = f
        yield request

    def parse(self, response):
        f = response.meta['file']

        html = response.body.decode('windows-1251')
        matches = re.findall("(a href='//www.spr.ru/otzyvy/.*?(\.html)?'>Отзывы)", html)

        url = ""
        for m in matches:
            print(m)
            m = str(m)
            start = m.index("'//") + 3
            if ' title=' in m:
                end = m.index("' title='", start)
                url = "https://" + m[start:end]
            else:
                end = m.index("'>", start)
                url = "https://" + m[start:end]
            f.write(url + "\n")
