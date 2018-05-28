import re

import scrapy


class DirectionSpider(scrapy.Spider):
    """
    Возвращает файл со ссылками на отзывы по учреждениям в направлении
    Перед запуском заменить ссылку на направление на нужное
    запуск: scrapy crawl direction
    """
    direction = 'https://www.spr.ru/all/medtsentri/'

    name = "direction"
    filename = "institutions.txt"

    def start_requests(self):
        # подготовка файла для ссылок
        f = open(self.filename, 'w')
        f.write("")

        # отправка запроса, вызов функции parse
        request = scrapy.Request(url=self.direction, callback=self.parse)

        # передаем файл в функцию parse
        request.meta['file'] = f
        yield request

    def parse(self, response):
        # получаем файл
        f = response.meta['file']
        # получаем содержимое страницы
        html = response.body.decode('windows-1251')

        # поиск ссылок на направления с отзывами
        matches = re.findall("(a href='//www.spr.ru/otzyvy/.*?(\.html)?'>Отзывы)", html)
        url = ""
        for m in matches:
            print(m)
            m = str(m)

            # приводим ссылки к нормальному виду
            start = m.index("'//") + 3
            if ' title=' in m:
                end = m.index("' title='", start)
                url = "https://" + m[start:end]
            else:
                end = m.index("'>", start)
                url = "https://" + m[start:end]
            # записываем ссылку в файл
            f.write(url + "\n")
